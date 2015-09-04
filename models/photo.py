from db import db, photos_table
from passlib.hash import sha256_crypt
import uuid
from tinydb import TinyDB, where
import json
import time
from models.base_model import BaseModel

class Photo(BaseModel):
    """ a diary photo    """
    
    table = photos_table
    def __init__(self, filename=None):
        super().__init__()
        self.table = photos_table
        self.filename = filename
        self.file_extension = None
        self.type = None
        self.abspath = None
        self.name = None
        self.tags = set()
        self.votings = [] #list of tuples [(vote, date), ...] anonymous on purpose
        self.shared = [] # list of tuples if shared [("destination", date), ..]
        self.love_it = False 
        # all non_ddb attributes of the class wont be stored in the DB.
        #self.non_ddb.append("attrX")
        self.has_encoder.append("tags")

    def tags_encoder(self):
        return(list(self.tags))

