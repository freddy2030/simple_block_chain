import hashlib, json
import leveldbapi

FOUNDATIONBLOCK_ACCOUNT = "ffffffffffffffffffffffffffffffffffffffff"

db = leveldbapi.mleveldb

#account
def getBalance(account):
    accountData = db.getValue(account)
    if not accountData:
        return 0
    return accountData["balance"]

def setBanlance(account, balance):
    accountData = db.getValue(account)
    accountData["balance"] = balance
    db.putJson(account, accountData)

def getTempBalance(account):
    accountData = db.getValue(account)
    if not accountData:
        return 0
    return accountData["tempBalance"]

def setTempBalance(account, balance):
    accountData = db.getValue(account)
    accountData["tempBalance"] = balance
    db.putJson(account, accountData)

def getNonce(account):
    accountData = db.getValue(account)
    if not accountData:
        return 0
    return accountData["nonce"]

def setNonce(account, nonce):
    accountData = db.getValue(account)
    accountData["nonce"] = nonce
    db.putJson(account, accountData)

def getTempNonce(account):
    accountData = db.getValue(account)
    if not accountData:
        return 0
    return accountData["tempNonce"]

def setNonce(account, nonce):
    accountData = db.getValue(account)
    accountData["tempNonce"] = nonce
    db.putJson(account, accountData)
#transcation

def isTranscationVaild(transaction):
    sender = transaction["sender"]
    amount = transaction["amount"]
    nonce = transaction["nonce"]
    
    if not sender or amount <= 0:
        return False
    # balance = util.getBalance(sender)
    if nonce != (getTempBalance(sender) + 1):
        return False
    balance = getTempBalance(sender)
    if balance < amount:
        return False
    return True

transcation = {
    "sender" : "776b95dc71eff9c4ecf5762c46acebdad73e73de",
    "nonce" : 1,
    "recipient" : "haoleia",
    "amount": 10
}

isTranscationVaild(transcation)

#hash

def transcationHash(transcation):
    pass

# db.putJson("776b95dc71eff9c4ecf5762c46acebdad73e73de", {
#     "balance": 80,
#     "nonce": 7,
#     "tempBalance": 60,
#     "tempNonce": 8 
# })    

# setBanlance("776b95dc71eff9c4ecf5762c46acebdad73e73de",11)
# setTempBalance("776b95dc71eff9c4ecf5762c46acebdad73e73de",11)

# print(getBalance("776b95dc71eff9c4ecf5762c46acebdad73e73de"))

# print(getTempBalance("776b95dc71eff9c4ecf5762c46acebdad73e73de"))


#####################

def getMinerTranscation(recipient): 
    transcation = {
        "sender" : "0", 
        "recipient" : recipient, 
        "amount" :  10000
    }
    return transcation

def isBlockExit(blockIndex):
    pass

def generateSha256FromString(inputstring):
    return hashlib.sha256("hjw".encode("utf-8")).hexdigest()
# print(generateSha256FromString("111"))
def hash(block):
    if 'gPointers' in block:
        del(block['gPoninters'])

    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def isString2SHA256(sha256string):
    if len(sha256string) != 64:
        return False
    
    try :
        bytes.fromhex(sha256string)
    except Exception as e:
        print(e)
        return False

    return True

def isString2Account(accountString):
    if len(accountString) != 40:
        return False
    
    try :
        bytes.fromhex(sha256string)
    except Exception as e:
        print(e)
        return False

    return True
    
# a = "13b2cc6cc00f32dfc9f814e9a1759c202d12d7c1f55128cd1a9df14c84d983df"
