import hashlib, json
import leveldbapi
from ecdsa import SigningKey, NIST384p, VerifyingKey, SECP256k1
from binascii import hexlify, unhexlify
# import ecdsa

FOUNDATIONBLOCK_ACCOUNT = "ffffffffffffffffffffffffffffffffffffffff"

db = leveldbapi.mleveldb
#hash

def transcationHash(transcation):
    # if "signature" in transcation:
    #     del(transcation["signature"])
    # if "public" in transcation:
    #     del(transcation["public"])
    transcationNew = {
        "sender" : transcation["sender"],
        "nonce" : transcation["nonce"],
        "recipient" : transcation["recipient"],
        "amount": transcation["amount"],
    }
    
    transcation_string = json.dumps(transcationNew, sort_keys=True).encode()
    return hashlib.sha256(transcation_string).hexdigest()

def arrayHash(arrayObj):
    arrayString = ""
    for obj in arrayObj:
        arrayString += json.dumps(transcation, sort_keys=True)
    return hashlib.sha256(arrayString.encode()).hexdigest()


#account
def updateAccount():
    pass

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
    signature = transaction["signature"]
    public = transaction["public"]
    recipient = transaction["recipient"]
    
    vk = VerifyingKey.from_string(unhexlify(public), curve=SECP256k1)
    try:
        vk.verify(signature, transcationHash(transcation).encode("utf-8"))
    except expression as identifier:
        print("error")

    if not sender or amount <= 0:
        return False
    # balance = util.getBalance(sender)
    if nonce != (getTempBalance(sender) + 1):
        return False
    balance = getTempBalance(sender)
    if balance < amount:
        return False
    if not isString2SHA256(recipient):
        return False
    return True

def getTranscationString(transaction):
    if "signature" in transcation:
        del(transcation["signature"])
    if "public" in transcation:
        del(transcation["public"])

    return json.dumps(transcation, sort_keys=True).encode()

def getTranscationSignature(private, transaction):
    sk = SigningKey.from_string(unhexlify(private), curve=SECP256k1)
    signature = sk.sign(transcationHash(transaction).encode("utf-8"))
    return signature

transcation = {
    "sender" : "776b95dc71eff9c4ecf5762c46acebdad73e73de",
    "nonce" : 1,
    "recipient" : "haoleia",
    "amount": 10,
    "signature": "1111"
}

a = getTranscationSignature("13b2cc6cc00f32dfc9f814e9a1759c202d12d7c1f55128cd1a9df14c84d983df", transcation)

transcation["signature"] = a
transcation["public"] = "6a505807200672fc382f25a0cb8d3e5d4f634eadb1f7cc2ed90726bc29cc57645967a78848e95cc4a93aa144bc7c908c45ede7874c1e82f9e559c5053e4cbe55"

print(isTranscationVaild(transcation))





# transcationList = [
#     {
#     "sender" : "776b95dc71eff9c4ecf5762c46acebdad73e73de",
#     "nonce" : 1,
#     "recipient" : "haoleia",
#     "amount": 10,
#     "signature": "1111"
# },
# {
#     "sender" : "776b95dc71eff9c4ecf5762c46acebdad73e73de",
#     "nonce" : 1,
#     "recipient" : "haoleia",
#     "amount": 10,
#     "signature": "1111"
# }
# ]
# print(arrayHash(transcationList))
# print(transcationHash(transcation))
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
