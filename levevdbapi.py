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
            value = leveldb.LevelDB(self.path).Get(keyByte)
        except KeyError:
            print("key: " + key + "  is not exit")
            return None
        else:
            print("get value success  ", key)
            # print(value.decode('utf-8'))
            valueStr = value.decode('utf-8')
            valueJson = json.loads(valueStr)
            return valueJson


    def putJson(self, key, block):
        keyByte = str.encode(key)
        blockStr = json.dumps(block)
        blockByte = str.encode(blockStr)
        leveldb.LevelDB(self.path).Put(keyByte, blockByte)
        print("save success  " + key)


mleveldb = LevelDB()


# mleveldb = None

# a = {"c":1}

# putBlock("1",a)

# print(db.Get(b'1'))
# print(getValue("1")["c"])
