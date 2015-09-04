from PIL import Image
import glob, os

size = (360, 180)
print(size)
infile = "test.png"
file, ext = os.path.splitext(infile)
im = Image.open(infile)
print(dir(im))
im.thumbnail(size)
im.save(file + ".thumbnail.png")