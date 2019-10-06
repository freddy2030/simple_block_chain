import hashlib
import json
from time import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
from uuid import uuid4
import util
import requests
import transaction as settingTran

# from flask import Flask, jsonify, request, g, Flask,session

from leveldbapi import mleveldb
# import leveldb
import os

TRANSCTIONS_POOL_KEY = "transactions_pool"
FOUNDATIONBLOCK_HASH = "4f025c4ef95f64c069dc448b3aef548332f0db12ef7567ff8fa345bd16fe8f11"

def getBalance(account):
    accountData = mleveldb.getValue("account")
    if not accountData:
        return 0
    return accountData["balance"]

def addFoundationBlock(self):
    foundationBlock = {
            "id": "eva",
            'index': 0,
            'gindex': 0,
            'timestamp': 0,
            'transactions': "bd55e377bf5dadaf1963bf9f570b425a70c07aeeb887555749d1f4520ae2e495",
            'proof': 0,
            'previous_hash': "0",
            'previous_g_hash': "0" 
        }
    if (self.get_block_from_index(0) == None):
        print("not exit")
        self.submit_block(foundationBlock, [])
    
    # if (self.get_cur_gblock_from_index(0) == None):
    #     self.submit_global_block(foundationBlock)

def readChainInfo(self):
    chain_info = self.db.getValue("chain_info")
    if chain_info:
        self.id = chain_info["id"]

def initBlockChain(self):
    addFoundationBlock(self)
    readChainInfo(self)

    index = 1
    while(1):
        key = "block-" + str(index)
        if not self.db.getValue(key):
            self.index = index -1
            break
        index += 1
    
    gindex = 1
    while(1):
        key = "gblock-" + str(gindex)
        if not self.db.getValue(key):
            self.globalchainindex = gindex -1
            break
        gindex += 1
    chain_info = self.db.getValue("chain_info")
    if chain_info:
        self.id = chain_info["id"]
    if self.id == "":
            while(1):
                input_id = input("Enter your chain id: ")
                if util.isString2SHA256(input_id):
                    self.id = input_id
                    chain_info = {
                        "id": input_id
                    }
                    self.db.putJson("chain_info",chain_info)
                    break
                else :
                    print("this id is not a sha256 string, please input again")

def updateBlock(self):
    pinChain = json.load(open('./config/pinChain.json', 'r'))
    nodeList = pinChain[self.id]
    maxIndex = self.index
    print("@89+++++++++++++++++++++++++++++++")
    print(maxIndex)
    longNode = ""
    for node in nodeList:
        print("@88##########################")
        print(node)
        try: 
            res = requests.get("http://%s/get_index" % node)
            data = json.loads(str(res.content,"utf-8"))
            if data["index"] and data["index"] > maxIndex:
                maxIndex = data["index"]
                longNode = node
            # print(data)
            # if index > maxIndex:
            #     maxIndex = index
            #     longNode = node
            pass
        except:
            print("node can not connect")
            pass
    if longNode != "":
        res = requests.get("http://%s/get_all_info" % longNode)
        data = json.loads(str(res.content,"utf-8"))
        for i in range(1, maxIndex + 1):
            blockData = data["block-" + str(i)] 
            mHash = blockData["curBlock"]
            blockTran = blockData[mHash]
          
            print(blockTran)
            self.submit_block(blockTran["block"], blockTran["transactions"])
            blockInfoKey = "block-" + str(i)
    
            # blockInfo = {
            #     "index": index,
            #     "curBlock": mHash,
            #     "blockpool": [ mHash ]
            # }
            blockData.pop(mHash)
            self.db.putJson(blockInfoKey, blockData)
        
        

        self.index = maxIndex
        # settingTran.resetBalance(self)
        print(data)
    
    self.state = "work"
       


class Blockchain:
    def __init__(self, db):
        self.db = db
        self.state = "update"
        # self.current_transactions = []
        # self.chain = []
        # self.globalchain = []
        self.nodes = set()
        self.globalchainindex = -1
        self.index = -1
        self.id = ""
        self.transactionList = []
        self.packagedTransaction = []
        self.tempAccount = []
        self.account = []

        initBlockChain(self)
        updateBlock(self)
        # 创建创世块
        # self.new_block(1, time(), self.current_transactions,
        #                previous_hash='1', proof=100)

    # def __new__(cls, *args, **kw):
    #         if not hasattr(cls, '_instance'):
    #             print(" ---------------------------------no instance")
    #             cls._instance = super().__new__(cls)  
    #         return cls._instance 
    
    def test(self, block):
        # del(block["a"])
        print(block)

  
        # if self.db:
        #     if not self.db.getValue("index"):
        #         print("no block chain")
        # else:
        #     raise Exception("ERROR: no db !!!")

    def addTransaction(self, transaction): 
        if not util.isTranscationVaild(transaction):
            return False
        self.transactionList.append(transaction)
        if transaction["sender"] not in self.tempAccount:
            self.tempAccount.append(transaction["sender"])
        if transaction["recipient"] not in self.tempAccount:
            self.tempAccount.append(transaction["recipient"])
        if transaction["sender"] not in self.account:
            self.account.append(transaction["sender"])
        if transaction["recipient"] not in self.account:
            self.account.append(transaction["recipient"])
       
    def register_node(self, address: str) -> None:
        """
        Add a new node to the list of nodes

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """
        parsed_url = urlparse(address)
        print(parsed_url)
        self.nodes.add(parsed_url.netloc)

    def get_transaction_from_hash(self, mHash):
        return self.db.getValue( mHash )
    
    def get_transactions_pool(self):
        return ({
            "sender":"0",
            "recipient":"ffffffffff",
            "amount":1
        })
        return self.db.getValue( TRANSCTIONS_POOL_KEY )

    def get_block_from_hash(self, mHash ):
        blockData = self.db.getValue( mHash )
        print(blockData)
        if blockData:
            return blockData["block"]
        return None
    
    def get_block_with_transcation_from_hash(self, mHash):
        block = self.db.getValue( mHash )
        if block:
            return block
        return None

    def get_block_from_index(self, index):
        blockInfo = self.get_block_info_from_index( index )
        if blockInfo:
            mHash = blockInfo["curBlock"]
            block = self.get_block_from_hash(mHash)
            return block
        return None

    def get_block_info_from_index(self, index):
        blockInfoKey = "block-" + str( index )
        blockInfo = self.db.getValue( blockInfoKey )
        if blockInfo:
            return blockInfo
        return None
    
    def get_gblock_info_from_index(self, index):
        gBlockInfoKey = "gblock-" + str( index )
        gBlockInfo = self.db.getValue( gBlockInfoKey )
        if gBlockInfo:
            return gBlockInfo
        return None
        
    def get_cur_gblock_from_index(self, index):
        if index < 0:
            return 0
        gblockInfoKey = "gblock-" + str( index )
        gblockInfo = self.db.getValue( gblockInfoKey )
        if not gblockInfo:
            return None
        mHash = gblockInfo["curBlock"]
        block = self.db.getValue( mHash )["block"]
        return block
    
    def get_all_gblock_from_index(self, index):
        if index <= 0:
            return False
        gblockInfoKey = "gblock-" + str( index )
        gblockInfo = self.db.getValue( gblockInfoKey )
        if gblockInfo:
            pool = gblockInfo["blockpool"]
            print( pool )
            blockSum = {
                "count": len( pool ),
                "blocks": {}
            }
            for blockHash in pool:
                blockSum["blocks"][blockHash] = self.get_block_from_hash( blockHash )
            return blockSum
        return None
    
    def get_all_block_from_index(self, index):
        if index < 0:
            return False

        blockInfoKey = "block-" + str( index )
        blockInfo = self.db.getValue( blockInfoKey )
        if blockInfo:
            pool = blockInfo["blockpool"]
            print( pool )
            blockSum = {
                "count": len( pool ),
                "blocks": {}
            }
            for blockHash in pool:
                blockSum["blocks"][blockHash] = self.get_block_from_hash( blockHash )
            return blockSum
        return None

    def isBlockVaild(self, beforeInfo, block):
        if util.hash(block)[:3] != "000":
            return False
        print(beforeInfo)
        if block["previous_hash"] not in beforeInfo["blockpool"]:
            return False
        
        return True

    def submit_block(self, block, transaction):
        mHash = util.hash(block)
        
        if self.db.getValue(mHash):
            return False

        if "index" not in block:
            return False
        index = block['index']
        
        if index == 0:
            if self.hash(block) == FOUNDATIONBLOCK_HASH:
                tran_data = util.getMinerTranscation(util.FOUNDATIONBLOCK_ACCOUNT)
                # self.packagedTransaction.append(tran_data)
                transaction.append(tran_data)
                blockData = {
                    "transactions": transaction,
                    "block": block
                }
                self.db.putJson(FOUNDATIONBLOCK_HASH, blockData) 
                # self.account.append(util.FOUNDATIONBLOCK_ACCOUNT)
                # self.tempAccount.append(util.FOUNDATIONBLOCK_ACCOUNT)
                # print("  初始块  :   " )
                # print(self.db.getValue(FOUNDATIONBLOCK_HASH))           
        else :
            beforeBlockInfo = self.db.getValue( "block-" + str(index - 1) )
            if self.isBlockVaild(beforeBlockInfo, block):
            # self.packagedTransaction.append(util.getMinerTranscation(""))
                blockData = {
                    "transactions": transaction,
                    "block": block
                }
                # for transaction in transaction:
                #     if(transaction["sender"] !="0"):
                #         self.addTransaction(transaction)
                self.db.putJson(mHash, blockData)
            else :
                return False
       
        blockInfoKey = "block-" + str(index)
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
        
        self.db.putJson(blockInfoKey, blockInfo)
        self.index += 1

        # util.output_all_info()
        # util.updateAllAccount(self.tempAccount)
        
        # self.tempAccount = []
        # for transcation in self.transactionList:
        #     if transcation in self.packagedTransaction:
        #         self.tempAccount.remove(transcation)
        # self.packagedTransaction = []
        settingTran.resetBalance(self)
        return blockData

    def submit_global_block(self, block): 
        # self.db.putJson(mHash, block)
        # self.db.putJson(index, {"hash":mHash})
        mHash = self.hash(block)
       
        if "gindex" not in block:
            return False
        index = block['gindex']
        if index == 0:
            pass
        else :
            beforeBlockInfo = self.get_all_gblock_from_index( index - 1 )
            if beforeBlockInfo:
                beforeBlockPool = beforeBlockInfo["blocks"]
                if mHash not in beforeBlockPool:
                    return False

        gBlockInfoKey = "gblock-" + str(index)
        gBlockInfo = self.db.getValue( gBlockInfoKey )
        
        if not gBlockInfo:
            gBlockInfo = {
                "index": index,
                "curBlock": mHash,
                "blockpool": [ mHash ]
            }
        else:
            gBlockInfo["blockpool"].append(mHash) 

        self.db.putJson(gBlockInfoKey, gBlockInfo)
        self.db.putJson(mHash, block)
         
        return True
        # blockInfoKey = "block-" + str(index)
        # blockInfo = self.db.getValue( blockInfoKey )
        
        # if not blockInfo:
        #     blockInfo = {
        #         "index": index,
        #         "curBlock": mHash,
        #         "blockpool": [ mHash ]
        #     }
        # else:
        #     blockInfo["blockpool"].append( mHash )
        
        # self.db.putJson(blockInfoKey, blockInfo)
        
        
    

    def new_block(self, index, timestamp, current_transactions,
                  previous_hash, proof, previous_g_hash, gPointers = None, gIndex = 0):
        """
        生成新块

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """
        # if gPointers: 
            # mIndex = "gblock-%s".format_map(,index)
            # block = {
            #     'index': index,
            #     'globalpointer':gPointers,
            #     'timestamp': timestamp,
            #     'transactions': current_transactions,
            #     'proof': proof,
            #     'previous_hash': previous_hash or self.hash(self.chain[-1]),
            # }
        # else :
        transaction = util.arrayHash(self.packagedTransaction)

        print("transaction")
        print(transaction)
        print(self.packagedTransaction)
        block = {
            "id":self.id,
            'index': index,
            'gindex': gIndex,
            'timestamp': timestamp,
            'transactions': transaction,
            'proof': proof,
            'previous_hash': previous_hash ,
            'previous_g_hash': previous_g_hash 
        }
        
        # if gPointers:
        #     block['globalpointer'] = gPointers


        # Reset the current list of transactions
        # self.current_transactions = []
        
        # mHash = self.hash(block)
       
       
        # self.chain.append(block)
        return block

    def new_candidate_block(self, index, timestamp, current_transactions,
                            previous_hash, previous_g_hash, gIndex = 0):
        """
        生成新块

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """
        self.packagedTransaction = self.transactionList
        packagedTran = util.getMinerTranscation("776b95dc71eff9c4ecf5762c46acebdad73e73de")
        if packagedTran not in self.packagedTransaction:
            self.packagedTransaction.append(packagedTran)
            util.updateAccount(packagedTran)
            if packagedTran["recipient"] not in self.tempAccount:
                self.tempAccount.append(packagedTran["recipient"])
            if packagedTran["recipient"] not in self.account:
                self.account.append(packagedTran["recipient"]) 
        print(self.packagedTransaction)
        block = {
            "id": self.id,
            'index': index,
            'gindex': gIndex,
            'timestamp': timestamp,
            'transactions': util.arrayHash(self.packagedTransaction),
            'previous_hash': previous_hash,
            'previous_g_hash': previous_g_hash,
            'proof': ''
        }


        return block

    @property
    def last_block(self):
        return self.get_block_from_index( self.index )
    
    @property
    def last_gblock(self):
        return self.get_cur_gblock_from_index( self.index )

    @staticmethod
    def hash(block: Dict[str, Any]) -> str:
        """
        生成块的 SHA-256 hash值

        :param block: Block
        """
        if 'gPointers' in block:
            del(block['gPoninters'])
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def get_hash_block_proof(block_tmp, proof):   #------------------------------------------

        block_tmp['proof'] = proof

        guess_hash = Blockchain.hash(block_tmp)
        return guess_hash

    @staticmethod
    def valid_proof(block_tmp, proof: int) -> bool:
        # guess = f'{last_proof}{proof}'.encode()
        # guess = (str(block_tmp) + str(proof)).encode()
        # guess_hash = hashlib.sha256(guess).hexdigest()
        # return guess_hash[:4] == "0000"

        guess_hash = Blockchain.get_hash_block_proof(block_tmp, proof)
        return guess_hash[:3] == "000"

    def proof_of_work(self, block_tmp) -> int: 
        """
        简单的工作量证明:
         - 查找一个 p 使得 hash 以4个0开头
        """

        proof = 0
        while self.valid_proof(block_tmp, proof) is False:
            proof += 1

        return proof

    def valid_chain(self, chain: List[Dict[str, Any]]) -> bool:  #------------------------------------------
        """
        Determine if a given blockchain is valid

        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            # print(f'{last_block}')
            # print(f'{block}')
            print(last_block)
            print(block)
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            block_tmp = self.new_candidate_block(block['index'],
                                                 block['gindex'],
                                                 block['timestamp'],
                                                 block['transactions'],
                                                 block['previous_hash'],
                                                 block['previous_g_hash'])

            if not self.valid_proof(block_tmp, block['proof']):
                return False
            
            last_block = block
            current_index += 1

        return True

    def set_longest_global_block_chain(self): #----------------------------------------
        maxGlobalHeight = self.globalchainindex
        # maxHeight = self.index
        # globalBlockHash = self.hash( self.last_gblock )
        preGlobalBlockHash = self.get_cur_gblock_from_index( maxGlobalHeight )["previous_g_hash"]
        for index in range(1, maxGlobalHeight )[::-1]:
            globalBlockInfo = self.get_gblock_info_from_index( index )
            globalBlockInfo["curBlock"] = preGlobalBlockHash
            self.change_gblock_info( globalBlockInfo )
            curGlobalBlock = self.get_cur_gblock_from_index( index )
            if curGlobalBlock:
                preGlobalBlockHash = curGlobalBlock["previous_g_hash"]

    
    def set_longest_block_chain_from_certain_block(self, mHash):
        certainBlock = self.get_block_from_hash( mHash )
        preBlockHash = mHash
        if certainBlock:
            certainIndex = certainBlock["index"]
            for index in range(1, certainIndex)[::-1]:
                blockInfo = self.get_block_info_from_index( index )
                blockInfo["curBlock"] = preBlockHash
                self.change_block_info( blockInfo )
                curBlock = self.get_block_from_index( index )
                if curBlock:
                    preBlockHash = curBlock["previous_hash"] 
            
            preBlockHash = mHash
            for index in range(certainIndex + 1, self.index + 1 ):
                blockInfo = self.get_block_info_from_index( index )
                blockPool = self.get_all_block_from_index( index )["blocks"]
                for blockHash in blockPool:
                    block = self.get_block_from_hash(blockHash)
                    if block["pervious_hash"] == preBlockHash:
                        blockInfo["curBlock"] = blockHash
                        self.change_block_info( blockInfo )
                        preBlockHash = blockHash

            

    def change_block_info(self, blockInfo):
        index = blockInfo["index"]
        key = "block-" + index
        self.db.putJson(key, blockInfo)
    
    def change_gblock_info(self, gblockInfo):
        index = gblockInfo["index"]
        key = "gblock-" + index
        self.db.putJson(key, blockInfo)

    def valid_transactions(self, transaction):
        pass

blockchain = Blockchain( mleveldb ) 

# a = blockchain.new_block(1, time(), [], previous_hash='1', proof=100, gPointers={"1":1}, gIndex=1, previous_g_hash="1")#{"A":{"index":1,"hash":"233333"}}
# blockchain.submit_global_block(a)
# print(a)
# blockchain.submit_block(a)
# print(blockchain.last_block)
# print(blockchain.get_block_from_hash("2dcca01ab24e111bf8b006231c250a9e07e30c1df47ece8ba0defb15ce4075a9"))
# print(blockchain.get_gblock_from_index(1))

# a = {"a":1}
# blockchain.test(a)
# print(blockchain.get_all_gblock_from_index(1))
# print(blockchain.get_block_from_index(1))
# print(blockchain.index)
# print(blockchain.globalchainindex)
# print( blockchain.get_all_block_from_index(1))
# print( blockchain.get_all_block_from_index(2))
# print( blockchain.get_all_block_from_index(3))
# print( blockchain.get_all_gblock_from_index(1))
# print( blockchain.get_all_gblock_from_index(2))
