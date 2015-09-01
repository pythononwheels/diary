from db import db, photos_table
from passlib.hash import sha256_crypt
import uuid
from tinydb import TinyDB, where
import json
import time
from models import BaseModel

class Photo(BaseModel):
    """ a diary photo    """
    
    table = photos_table
    def __init__(self, filename=None):
        self.table = photos_table
        self.filename = filename
        self.type = None
        self.abspath = None
        self.time = time.time()
        self.time_str = self.get_time()
        self.name = None
        
        self.tags = set()
        self.votings = [] #list of tuples [(vote, date), ...] anonymous on purpose
        self.shared = [] # list of tuples if shared [("destination", date), ..]
        self.love_it = False 
        
        self._id = str(uuid.uuid4())
        # all non_data attributes of the class wont be stored in the DB.
        self.non_data = ["table"]
        self.has_encoder = ["tags"]

