#
# thumbnails
# 
import os
from thumbnails import get_thumbnail

img = get_thumbnail(os.path.abspath('./static/images/IMG_2625.jpg'), '300x300', crop='center')
print(img)
print(dir(img))
print(img.name)
print(img.path)
