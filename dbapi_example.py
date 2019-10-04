import leveldbapi, util

db = leveldbapi.mleveldb

a = util.getMinerTranscation(util.FOUNDATIONBLOCK_ACCOUNT)
print(a)

a = {
   "id":"a4ddd1cebc807d09950b870b2039604242d4950c3fa403a3c0ca9c13ed9586f0"
}

db.putJson("chain_info",a)

print(db.getValue(""))