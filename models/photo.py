from db import db, photos_table
from passlib.hash import sha256_crypt
import uuid
from tinydb import TinyDB, where
import json
import time
from models.base_model import BaseModel

class Photo(BaseModel):
    """ a diary post    """
    
    table = photos_table
    def __init__(self, path):
        self.table = photos_table
        self.path = path
        self.name = None

