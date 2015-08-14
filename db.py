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

story_table = db.table('story')

access_table = db.table('access')
