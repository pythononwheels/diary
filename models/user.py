from db import db, users_table
from passlib.hash import sha256_crypt
import uuid
from tinydb import TinyDB, where
import json
from models.base_model import BaseModel

class User(BaseModel):
    """
       a diary user
    """
    
    table = users_table
    def __init__(self, login):
        super().__init__()
        self.table = users_table
        self.login = login
        self.email = None
        self.firstname = None
        self.lastname = None
        self.gender = None
        self.profile_photo = None
        self.motto = None
        self.hash = None
        #self.non_db.append("attrX")
        #self.has_encoder.append("tags")

    def create_from_db(self):
        if self.exists_in_db():
            res = self.table.search(where("login") == self.login)
            res = res[0]
            #print(res)
            for key,value in res.items():
                setattr(self, key, value)
            #print(self.to_dict())
            return self
        else:
            return None

    def exists_in_db(self):
        """ check if user is in db """
        return self.table.contains(where("login") == self.login)

    def set_password(self, raw_pwd):
        self.hash = sha256_crypt.encrypt(raw_pwd)
        #self.to_db()

    def check_password(self, raw_pwd):
        """ pwd check """
        return sha256_crypt.verify(raw_pwd, self.hash)

