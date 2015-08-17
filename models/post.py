from db import db, posts_table
from passlib.hash import sha256_crypt
import uuid
from tinydb import TinyDB, where
import json
import time

class Post(object):
    """ a diary post    """
    
    table = posts_table
    def __init__(self, title=None):
        self.table = users_table
        self.title = title
        self.date = None
        self.text = None
        self.is_event = False
        self.event_text = None
        self.tags = set()
        self.votings = [] #list of tuples [(vote, date), ...] anonymous on purpose
        self.shared = [] # list of tuples if shared [("destination", date), ..]
        self.is_favourite = None 
        self.photos = [] # list of ids of photo models
        self._id = str(uuid.uuid4())
        self.non_data = ["table"]

    def get_time(self):
        return time.strftime("%Y-%m-%d %H:%M")

    def exists_in_db(self):
        """ check if user is in db """
        return self.table.contains(where("_id") == self._id)

    def create_from_db(self):
        if self.exists_in_db():
            res = self.table.search(where("_id") == self._id)
            res = res[0]
            #print(res)
            for key,value in res.items():
                setattr(self, key, value)
            #print(self.to_dict())
            return self
        else:
            return None

    @classmethod
    def find_by_id(self, id):
        if self.table.contains(where("_id") == id):
            res = self.table.search(where("_id") == id)
            return res[0]
        else:
            return False
        
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