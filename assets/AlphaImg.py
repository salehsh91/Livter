from PIL import Image
filename = "assets/health.png"
img = Image.open(filename).convert("RGBA")

pixels = img.load()

for y in range(img.height):
    for x in range(img.width):
        r,g,b,a = pixels[x,y]

        if r > 245 and g > 245 and b > 245:
            pixels[x,y] = (255,255,255,0)

img.save(filename)