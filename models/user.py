from db import db, users_table
from passlib.hash import sha256_crypt
import uuid
from tinydb import TinyDB, where
import json

class User(object):
    """ Repräsentiert einen MAVS User
        attribute: 
                swbkuerzel
                role (user | admin)

    """
    
    table = users_table
    def __init__(self, login):
        self.table = users_table
        self.login = login
        self.email = None
        self.firstname = None
        self.lastname = None
        self.gender = None
        self.profile_photo = None
        self.motto = None
        self.hash = None
        self._id = str(uuid.uuid4())
        self.non_data = ["table"]
        # try to find the user 
        if self.exists_in_db():            
            # user exists in db so, take the attributes from db
            self.create_from_db()

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

    @classmethod
    def find(self, login):
        u = User(login)
        return u
        
    def find_all(self):
        return self.table.all()
    
    def to_dict(self):
        d  = {}
        for elem in self.__dict__:
            if elem not in self.non_data and elem != "non_data":
                d[elem] = getattr(self, elem)
        return d

    def to_JSON(self):
        return json.dumps(self.to_dict())

    def to_db(self):
        d = self.to_dict()
        if self.exists_in_db():
            print("updating")
            self.table.update(d ,where("_id")== self._id)
        else:
            print("inserting")
            self.table.insert(d)
        return

    def set_password(self, raw_pwd):
        self.hash = sha256_crypt.encrypt(raw_pwd)
        #self.to_db()

    def check_password(self, raw_pwd):
        """ pwd check """
        return sha256_crypt.verify(raw_pwd, self.hash)

    def __str__(self):
        return str(self.__dict__)