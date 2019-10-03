import hashlib



def generateSha256FromString(inputstring):
    return hashlib.sha256("hjw".encode("utf-8")).hexdigest()
print(generateSha256FromString("111"))
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
