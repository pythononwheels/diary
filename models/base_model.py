from passlib.hash import sha256_crypt
import uuid
from tinydb import TinyDB, where
import json
import time
import pprint

class BaseModel(object):
    """ a diary post    """
    
    def __init__(self):
        self.time = time.time()
        self.time_str = self.get_time() 
        self._id = str(uuid.uuid4())
        self.non_db = ["table", "has_encoder"]
        self.has_encoder = []

    def get_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.time))
    
    def exists_in_db(self):
        """ check if user is in db """
        return self.table.contains(where("_id") == self._id)

    
    def create_from_id(self,id ):    
        return self.create_from_dict(self.find_by_id(id))

    
    def create_from_dict(self, d):    
        for key,value in d.items():
            setattr(self, key, value)
        #print(self.to_dict())
        return self
        

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

    def tags_encoder(self):
        return(list(self.tags))

    @classmethod
    def find(self, *args, **kwargs):
        return self.table.search(*args, **kwargs)

    def find_one(self, *args, **kwargs):
        res = None
        res = self.table.search(*args, **kwargs)
        if res:
            t_class = type(self.__class__.__name__, (self.__class__,), {})
            t_obj = t_class()
            t_obj.create_from_dict(res[0])
            return t_obj
        else:
            return None


    @classmethod
    def find_by_id(self, id):
        if self.table.contains(where("_id") == id):
            res = self.table.search(where("_id") == id)
            return res[0]
        else:
            return False
    
    @classmethod
    def find_all(self):
        return self.table.all()
    
    def to_dict(self):
        d  = {}
        for elem in self.__dict__:
            if elem not in self.non_db and elem != "non_db":
                d[elem] = getattr(self, elem)
        return d
    
    def get_eid(self):
        if self.exists_in_db():
            res = self.table.get(where("_id")==self._id)
            if hasattr(res, "eid"):
                return res.eid
        return None

    def to_db_dict(self):
        d  = {}
        for elem in self.__dict__:
            if elem not in self.non_db and elem != "non_db":
                if elem in self.has_encoder:
                    d[elem] = getattr(self, str(elem)+"_encoder")()
                else:
                    d[elem] = getattr(self, elem)
        return d

    def to_JSON(self):
        return json.dumps(self.to_dict())

    def upsert(self):
        d = self.to_db_dict()
        if self.exists_in_db():
            print("updating")
            self.table.update(d ,where("_id")== self._id)
        else:
            print("inserting")
            self.table.insert(d)
        return

    def delete(self):
        res = self.table.remove(where('_id') ==self._id)
        print("deleting id: " + str(self._id) + " from: " + str(self.table) )
        print("result: " + str(res))

    def __str__(self):
        pp = pprint.PrettyPrinter(indent=4)
        return str(pp.pprint(self.__dict__))