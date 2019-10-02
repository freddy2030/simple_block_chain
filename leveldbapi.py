import leveldb
import json

# db = leveldb.LevelDB('./db')
# db.Put(b"0", b"1")
# a = db.Get(b"0")
# db = leveldb.LevelDB('./db')

class LevelDB:
    def __init__(self,path = "./db"):
        self.path = path
        # self.db = leveldb.LevelDB(path)
        # print("level db init")
       
    
    # def __new__(cls, *args, **kw):
    #     if not hasattr(cls, '_instance'):
    #         cls.db = leveldb.LevelDB('./db')
    #         cls._instance = super().__new__(cls)  
    #     return cls._instance 

    def getValue(self, key):
        keyByte = str.encode(key)
        try:
            db = leveldb.LevelDB(self.path)
            value = db.Get(keyByte)
        except KeyError:
            print("key: " + key + "  is not exit")
            return None
        else:
            print("get value success  ", key)
            # print(value.decode('utf-8'))
            valueStr = value.decode('utf-8')
            valueJson = json.loads(valueStr)
            return valueJson
        finally:
            del(db)


    def putJson(self, key, block):
        keyByte = str.encode(key)
        blockStr = json.dumps(block)
        blockByte = str.encode(blockStr)
        db = leveldb.LevelDB(self.path)
        db.Put(keyByte, blockByte)
        print("save success  " + key)
        del(db)


mleveldb = LevelDB()

# mleveldb.putJson("test1", {"name":"123"})
# mleveldb.getValue("block-1")


# mleveldb = None

# a = {"c":1}

# putBlock("1",a)

# print(db.Get(b'1'))
# print(getValue("1")["c"])
