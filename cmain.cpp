#include <iostream>
#include <string>
#include <array>
#include <unordered_map>
#include <SDL3/SDL.h>

std::unordered_map<std::string,SDL_Texture*> textures;
SDL_Window* WINdow = nullptr;
SDL_Renderer* RENderer = nullptr;

void frame(SDL_Renderer *renderer){
    SDL_SetRenderDrawColor(renderer,25,30,40,255);
    SDL_RenderClear(renderer);


    SDL_RenderPresent(renderer);
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

int Render(SDL_Renderer* renderer = GetRenderer()){
    int running = 1;
    SDL_Event ev;
    
    while(SDL_PollEvent(&ev)){
        if(ev.type == SDL_EVENT_QUIT){
            running = 0;
        }
    }

    frame(renderer);
    SDL_Delay(16);

    
    return running;
    

    
    
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
void Pr(int* blocks ,int conut){
    for(int i = 0; i < conut; i++){
        std::cout << "arr " << i << " " <<  blocks[i] << std::endl;
        
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
void pr(int* blocks ,int conut){
    Pr(blocks,conut);
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