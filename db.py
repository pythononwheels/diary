#
#
# db
#
import os
import tinydb
from tinydb import TinyDB

db = TinyDB(os.path.join("./", "db.json"))

# tables
users_table = db.table("users")

posts_table = db.table('posts')

photos_table = db.table('photos')

access_table = db.table('access')
