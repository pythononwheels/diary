from PIL import Image
import glob, os

size = (360, 180)
print(size)
infile = "test.png"
file, ext = os.path.splitext(infile)
im = Image.open(infile)
(width, height) = im.size
print("size: " + str(width) + " x " + str(height) )
print("ratio: " + str(width/height)) 
print(dir(im))
im.thumbnail(size)
im.save(file + ".thumbnail.png")