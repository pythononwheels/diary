#
# thumbnails
# 
import os
from thumbnails import get_thumbnail

SIZE="450x300"

img = get_thumbnail(os.path.abspath('./static/images/post_photos/IMG_2625.jpg'), '300x300', crop='center')
print(img.path)
img = get_thumbnail(os.path.abspath('./static/images/post_photos/IMG_2649.jpg'), '300x300', crop='center')
print(img.path)
img = get_thumbnail(os.path.abspath('./static/images/post_photos/IMG_3582.jpg'), '300x300', crop='center')
print(img)
print(dir(img))
print(img.name)
print(img.path)
