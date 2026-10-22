#include <iostream>
#include <string>
#include <array>
#include <unordered_map>
#include <cstdint>
#include <vector>
#include <SDL3/SDL.h>
#include <SDL3_image/SDL_image.h>

std::unordered_map<std::string,SDL_Texture*> textures;
SDL_Window* WINdow = nullptr;
SDL_Renderer* RENderer = nullptr;

void frame(SDL_Renderer* renderer) {
    SDL_SetRenderDrawColor(renderer, 25, 30, 40, 255);
    SDL_RenderClear(renderer);
}

SDL_Renderer* GetRenderer(){
    return RENderer;
}
SDL_Window* GetWindow(){
    return WINdow;
}



int INIT(){
    if(!SDL_Init(SDL_INIT_VIDEO)){
        SDL_Log("SDL_Init falied: %s",SDL_GetError());
        return 1;
    }
    WINdow = SDL_CreateWindow("Livter",1280,720,SDL_WINDOW_RESIZABLE);

    
    if(!WINdow){
        SDL_Quit();
        return 1;
    }

    RENderer = SDL_CreateRenderer(WINdow,nullptr);
    if(!RENderer){
        return 1;
    }

    return 0;
}

int Render(SDL_Renderer* renderer = GetRenderer()) {
    static int running = 1;

    SDL_Event ev;

    while (SDL_PollEvent(&ev)) {
        if (ev.type == SDL_EVENT_QUIT) {
            running = 0;
        }
    }

    if (!running)
        return 0;

    frame(renderer);
    return 1;
}

SDL_Texture* create_color_texture(SDL_Renderer* renderer,Uint8 r,Uint8 g,Uint8 b,Uint8 a){
    SDL_Surface* surface = SDL_CreateSurface(1,1,SDL_PIXELFORMAT_RGBA32);
    if(!surface){
        return nullptr;
    }
    Uint32 color = SDL_MapSurfaceRGBA(surface,r,g,b,a);
    SDL_FillSurfaceRect(surface,nullptr,color);
    
    SDL_Texture *texture = SDL_CreateTextureFromSurface(renderer,surface);
    SDL_DestroySurface(surface);
    return texture;
}

bool LoadImage(
    SDL_Renderer* renderer,
    const char* path,
    int name
) {
    if (!renderer || !path)
        return false;

    SDL_Texture* texture = IMG_LoadTexture(renderer, path);

    if (!texture) {
        SDL_Log(
            "Failed to load texture %s: %s",
            path,
            SDL_GetError()
        );
        return false;
    }

    std::string key = std::to_string(name);

    auto it = textures.find(key);

    if (it != textures.end() && it->second) {
        SDL_DestroyTexture(it->second);
    }

    textures[key] = texture;
    return true;
}

void loadtexture(SDL_Renderer* renderer,Uint8 r,Uint8 g,Uint8 b,Uint8 a,int name){
    SDL_Texture* texture = create_color_texture(renderer,r,g,b,a);
    textures[std::to_string(name)] = texture;
}

bool DrawObj(SDL_Renderer* renderer,float x,float y, float w, float h,int TextureName){
    if(!textures[std::to_string(TextureName)]){
        std::cout << "Texture None-ed" << std::endl;
        return false;
    }
    SDL_FRect dst = {x,y,w,h};
    SDL_RenderTexture(renderer,textures[std::to_string(TextureName)],nullptr,&dst);
    return true;
}
void Pr(
    const int32_t* blocks,
    const int32_t* chunk_coords,
    int chunk_count,
    int chunk_size,
    int block_size,
    float camera_x,
    float camera_y,
    float world_offset_x,
    float world_offset_y
) {
    if (!RENderer || !blocks || !chunk_coords)
        return;

    if (chunk_count <= 0 || chunk_size <= 0 || block_size <= 0)
        return;

    int screen_w = 0;
    int screen_h = 0;
    SDL_GetWindowSize(WINdow, &screen_w, &screen_h);

    const int blocks_per_chunk = chunk_size * chunk_size;

    struct TextureBatch {
        SDL_Texture* texture = nullptr;
        std::vector<SDL_Vertex> vertices;
        std::vector<int> indices;
    };

    std::unordered_map<int32_t, TextureBatch> batches;

    for (int c = 0; c < chunk_count; ++c) {
        const int chunk_x = chunk_coords[c * 2];
        const int chunk_y = chunk_coords[c * 2 + 1];

        const float origin_x =
            world_offset_x +
            static_cast<float>(chunk_x) * chunk_size * block_size +
            camera_x;

        const float origin_y =
            world_offset_y +
            static_cast<float>(chunk_y) * chunk_size * block_size +
            camera_y;

        const float chunk_w =
            static_cast<float>(chunk_size) * block_size;

        const float chunk_h = chunk_w;

        if (origin_x + chunk_w <= 0 ||
            origin_x >= screen_w ||
            origin_y + chunk_h <= 0 ||
            origin_y >= screen_h) {
            continue;
        }

        const int chunk_base = c * blocks_per_chunk;

        for (int i = 0; i < blocks_per_chunk; ++i) {
            const int32_t block_id = blocks[chunk_base + i];

            if (block_id == 0)
                continue;

            auto tex_it = textures.find(std::to_string(block_id));

            if (tex_it == textures.end() || !tex_it->second)
                continue;

            const float x =
                origin_x + (i % chunk_size) * block_size;
            const float y =
                origin_y + (i / chunk_size) * block_size;

            const float w = static_cast<float>(block_size);
            const float h = static_cast<float>(block_size);

            if (x + w <= 0 || x >= screen_w ||
                y + h <= 0 || y >= screen_h) {
                continue;
            }

            auto& batch = batches[block_id];
            batch.texture = tex_it->second;

            const int base = static_cast<int>(batch.vertices.size());

            const SDL_FColor color = {1, 1, 1, 1};

            batch.vertices.push_back({{x,     y},     color, {0, 0}});
            batch.vertices.push_back({{x + w, y},     color, {1, 0}});
            batch.vertices.push_back({{x + w, y + h}, color, {1, 1}});
            batch.vertices.push_back({{x,     y + h}, color, {0, 1}});

            batch.indices.push_back(base);
            batch.indices.push_back(base + 1);
            batch.indices.push_back(base + 2);

            batch.indices.push_back(base);
            batch.indices.push_back(base + 2);
            batch.indices.push_back(base + 3);
        }
    }

    for (auto& [block_id, batch] : batches) {
        if (batch.vertices.empty())
            continue;

        SDL_RenderGeometry(
            RENderer,
            batch.texture,
            batch.vertices.data(),
            static_cast<int>(batch.vertices.size()),
            batch.indices.data(),
            static_cast<int>(batch.indices.size())
        );
    }
}
int quit(SDL_Renderer* renderer = GetRenderer(),SDL_Window* window = GetWindow())
{
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}
extern "C"{


int Init(){
    return INIT();
}
void LoadTexture(SDL_Renderer* renderer,Uint8 r,Uint8 g,Uint8 b,Uint8 a,int name){
    loadtexture(renderer,r,g,b,a,name);
}bool LoadImageTexture(
    SDL_Renderer* renderer,
    const char* path,
    int name
) {
    return LoadImage(renderer, path, name);
}
SDL_Window* GetWINDOW(){
    return GetWindow();
}
SDL_Renderer* GetRENDERER(){
    return GetRenderer();
}
int render(){
    return Render();
}
bool drawobj(SDL_Renderer* renderer,float x,float y, float w, float h, int TextureName){
    return DrawObj(renderer,x,y,w,h,TextureName);
}
void pr(
    const int32_t* blocks,
    const int32_t* chunk_coords,
    int chunk_count,
    int chunk_size,
    int block_size,
    float camera_x,
    float camera_y,
    float world_offset_x,
    float world_offset_y
) {
    Pr(
        blocks,
        chunk_coords,
        chunk_count,
        chunk_size,
        block_size,
        camera_x,
        camera_y,
        world_offset_x,
        world_offset_y
    );
}

void present() {
    if (RENderer) {
        SDL_RenderPresent(RENderer);
        SDL_Delay(16);
    }
}
int Quit(){
    return quit();
}
void GetWindowsize(int*w,int*h,SDL_Window* window = GetWindow()){
    if (WINdow == nullptr) {
        *w = -1;
        *h = -1;
        return;
    }

    SDL_GetWindowSize(WINdow, w, h);
    
}

}