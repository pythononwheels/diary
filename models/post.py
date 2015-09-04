from db import db, posts_table
from passlib.hash import sha256_crypt
import uuid
from tinydb import TinyDB, where
import json
import time
from models.base_model import BaseModel

class Post(BaseModel):
    """ a diary post    """
    
    table = posts_table
    def __init__(self, title=None):
        super().__init__()
        self.table = posts_table
        self.title = title
        self.text = None
        self.is_event = False
        self.event_text = None
        self.tags = set()
        self.votings = [] #list of tuples [(vote, date), ...] anonymous on purpose
        self.shared = [] # list of tuples if shared [("destination", date), ..]
        self.love_it = False 
        self.photo = None # list of ids of photo models
        self.title_photo = None
        
        # all nondb attributes of the class wont be stored in the DB.
        #self.non_db.append("attrX")
        self.has_encoder.append("tags")
        

    def tags_encoder(self):
        return(list(self.tags))


   