import hashlib, json
import leveldbapi
from ecdsa import SigningKey, NIST384p, VerifyingKey, SECP256k1
from binascii import hexlify, unhexlify
import copy
# import ecdsa

FOUNDATIONBLOCK_ACCOUNT = "ffffffffffffffffffffffffffffffffffffffff"

db = leveldbapi.mleveldb

#output
def updateAllAccount(accountList):
    for accountId in accountList:
        account = db.getValue(accountId)
        account["balance"] = account["tempBalance"]
        account["nonce"] = account["tempNonce"]
        db.putJson(accountId, account)
 
def output_all_info():
    pass

#hash

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
        bytes.fromhex(accountString)
    except Exception as e:
        print(e)
        return False

    return True


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
        newObj = obj.copy()
        if "signature" in newObj:
            del(newObj["signature"])
        arrayString += json.dumps(newObj, sort_keys=True)
    return hashlib.sha256(arrayString.encode()).hexdigest()


#account
def getAccountList():
    accountList = db.getValue("account-list")
    if not accountList:
        db.putJson("account-list", {"data":[]})
        return []
    return accountList["data"]

def addAccountList(transcation):
    sender = transcation["sender"]
    recipient =  transcation["recipient"]
    accountList = getAccountList()
    if sender != "0" and sender not in accountList:
        accountList.append(sender)
    if recipient not in accountList:
        accountList.append(recipient)
    db.putJson("account-list", {"data":accountList})

def clearAccount(transcation):
    sender = transcation["sender"]
    recipient =  transcation["recipient"]
    account = {
            "balance": 0,
            "nonce": 0,
            "tempNonce": 0,
            "tempBalance": 0
        }
    if sender != "0":
        db.putJson(sender, account)
    db.putJson(recipient, account)

def initAccount(hashid, tempBalance):
    account = {
            "balance": 0,
            "nonce": 0,
            "tempNonce": 0,
            "tempBalance": tempBalance
        }
    db.putJson(hashid, account)

def changeBalance(transcation):
    sender = transcation["sender"]
    recipient =  transcation["recipient"]
    amount = transcation["amount"]
    nonce = transcation["nonce"]

    if sender != "0":
        senderAccount = db.getValue(sender)
        senderAccount["balance"] -= amount
        if nonce > senderAccount["nonce"]:
            senderAccount["nonce"] = nonce
        db.putJson("sender",senderAccount)
        
    recipientAccount = db.getValue(recipient)
    recipientAccount["balance"] += amount
    db.putJson(recipient,recipientAccount)
    

def updateAccount(transcation):
    print(transcation)
    sender = transcation["sender"]
    recipient =  transcation["recipient"]
    amount = transcation["amount"]

    senderAccount = db.getValue(sender)
    if sender != "0":
        senderAccount["tempNonce"] += 1
        senderAccount["tempBalance"] -= amount
        db.putJson(sender, senderAccount)
        nonce = transcation["nonce"]
    recipientAccount = db.getValue(recipient)
    if recipientAccount:
        recipientAccount["tempBalance"] += amount
    else :
        recipientAccount = {
            "balance": 0,
            "nonce": 0,
            "tempNonce": 0,
            "tempBalance": amount
        }
    db.putJson(recipient, recipientAccount)

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
    tempNonce = getNonce(sender)
    if nonce != (tempNonce + 1):
        return False
    balance = getTempBalance(sender)
    if balance < amount:
        return False
    if not isString2Account(recipient):
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

def generateTranscation(sender, recipient, amount, private):
    nonce = getNonce(sender)
    transcation = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount,
        "nonce": (nonce + 1)
    }
    transcation["signature"] = getTranscationSignature(private, transcation)
    return transcation

xhaccount = {
    "balance": 20,
    "nonce": 0,
    "tempNonce": 0,
    "tempBalance": 20
}

# db.putJson("776b95dc71eff9c4ecf5762c46acebdad73e73de", xhaccount)

transcation = {
    "sender" : "776b95dc71eff9c4ecf5762c46acebdad73e73de",
    "nonce" : 1,
    "recipient" : "0748a4169ca8d015bd2c8043179c6892880cac01",
    "amount": 10,
    "signature": "1111"
}

a = getTranscationSignature("13b2cc6cc00f32dfc9f814e9a1759c202d12d7c1f55128cd1a9df14c84d983df", transcation)

# b = a.decode()
# print(type(a))
# print(b)

# transcation["signature"] = a
# transcation["public"] = "6a505807200672fc382f25a0cb8d3e5d4f634eadb1f7cc2ed90726bc29cc57645967a78848e95cc4a93aa144bc7c908c45ede7874c1e82f9e559c5053e4cbe55"

# print(isTranscationVaild(transcation))

# updateAccount(transcation)



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
        "amount" :  10000,
        "nonce": 0
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

def submitGBlockInfo(self, block, gpointer):
    mHash = hash(block)
    index = block["gindex"]
    blockInfoKey = "gblock-" + str(index)
    blockInfo = self.db.getValue( blockInfoKey )

    if not blockInfo:           #
        blockInfo = {
            "index": index,
            "curBlock": mHash,
            "blockpool": [ mHash ]
        }
    else:
        if mHash not in blockInfo["blockpool"]:
            blockInfo["blockpool"].append( mHash )
    block = self.db.getValue(mHash)
    if block:
        block["gpointer"] = gpointer
    else:
        block = {
                    "gpointer": gpointer,
                    "block": block
                }
    self.db.putJson(mHash, block)
    self.db.putJson(blockInfoKey, blockInfo)
    self.globalchainindex += 1

    
# a = "13b2cc6cc00f32dfc9f814e9a1759c202d12d7c1f55128cd1a9df14c84d983df"
