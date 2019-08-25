import leveldb

db = leveldb.LevelDB('./db')
db.Put(b"0", b"1")
a = db.Get(b"0")
print(a)