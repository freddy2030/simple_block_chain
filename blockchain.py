import hashlib
import json
from time import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
from uuid import uuid4

import requests
# from flask import Flask, jsonify, request, g, Flask,session

from levevdbapi import mleveldb
# import leveldb
import os


# def initBlockChain(self):
#         if self.db:
#             if not self.db.getValue("index"):
#                 print("no block chain")
#         else:
#             raise Exception("ERROR: no db !!!")


class Blockchain:
    def __init__(self, db):
        self.db = db
        self.chainName = ""
        self.current_transactions = []
        self.chain = []
        self.globalchain = []
        self.nodes = set()
        self.globalchainindex = -1
        self.index = -1
    
        # initBlockChain(self)
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


    def setChainName(self, name):
        self.chainName = name


    def register_node(self, address: str) -> None:
        """
        Add a new node to the list of nodes

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """
        parsed_url = urlparse(address)
        print(parsed_url)
        self.nodes.add(parsed_url.netloc)

    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        """
        生成新交易信息，信息将加入到下一个待挖的区块中

        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    def get_block_from_hash(self, mHash ):
        return self.db.getValue( mHash )
    
    def get_block_from_index(self, index):
        if index == -1:
            return 0
        blockInfoKey = "block-" + str( index )
        blockInfo = self.db.getValue( blockInfoKey )
        mHash = blockInfo["curBlock"]
        block = self.db.getValue( mHash )
        return block

    def get_gblock_from_index(self, index):
        if index == -1:
            return 0
        gblockInfoKey = "gblock-" + str( index )
        gblockInfo = self.db.getValue( gblockInfoKey )
        mHash = gblockInfo["curBlock"]
        block = self.db.getValue( mHash )
        return block

    def submit_block(self, block): 
        # self.db.putJson(mHash, block)
        # self.db.putJson(index, {"hash":mHash})
        mHash = self.hash(block)
        index = block['index']

        blockInfoKey = "block-" + str(index)
        blockInfo = self.db.getValue( blockInfoKey )
        
        if not blockInfo:
            blockInfo = {
                "index": index,
                "curBlock": mHash,
                "blockpool": [ mHash ]
            }
        else:
            blockInfo["blockpool"].append( mHash )
        
        self.db.putJson(blockInfoKey, blockInfo)
        self.db.putJson(mHash, block)
        
        if "gIndex" in block:
            gIndex = block['gIndex']
            gBlockInfoKey = "gblock-" + str(gIndex)
            gBlockInfo = self.db.getValue( gBlockInfoKey )
           
            if not gBlockInfo:
                gBlockInfo = {
                    "index": gIndex,
                    "curBlock": mHash,
                    "blockpool": [ mHash ]
                }
            else:
                gBlockInfo["blockpool"].append(mHash) 

            self.db.putJson(gBlockInfoKey, gBlockInfo)
        
        

        
        
        pass

    def new_block(self, index, timestamp, current_transactions,
                  previous_hash, proof, previous_g_hash, gPointers = None, gIndex = None):
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
        block = {
            'index': index,
            'timestamp': timestamp,
            'transactions': current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.last_block),
            'previous_g_hash': previous_g_hash or self.hash(self.last_gblock)
        }
        
        if gPointers and gIndex:
            block['globalpointer'] = gPointers
            block['gIndex'] = gIndex

        # Reset the current list of transactions
        # self.current_transactions = []
        
        # mHash = self.hash(block)
       
       
        # self.chain.append(block)
        return block

    def new_candidate_block(self, index, gIndex, timestamp, current_transactions,
                            previous_hash, previous_g_hash):
        """
        生成新块

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """
        block = {
            'index': index,
            'gIndex': gIndex,
            'timestamp': timestamp,
            'transactions': current_transactions,
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
        return self.get_gblock_from_index( self.index )

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
        """
        验证证明: 是否hash(last_proof, proof)以4个0开头

        :param last_proof: Previous Proof
        :param proof: Current Proof
        :return: True if correct, False if not.
        """
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
                                                 block['gIndex'],
                                                 block['timestamp'],
                                                 block['transactions'],
                                                 block['previous_hash'],
                                                 block['previous_g_hash'])

            if not self.valid_proof(block_tmp, block['proof']):
                return False
            
            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self) -> bool: #----------------------------------------
        """
        共识算法解决冲突
        使用网络中最长的链.

        :return:  如果链被取代返回 True, 否则为False
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            # response = requests.get(f'http://{node}/chain')
            try:
                response = requests.get('http://%s/chain' % (node))

                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']

                    # Check if the length is longer and the chain is valid
                    if length > max_length and self.valid_chain(chain):
                        max_length = length
                        new_chain = chain

            except Exception as e:
                print(e)

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False


blockchain = Blockchain( mleveldb ) 

a = blockchain.new_block(1, time(), [], previous_hash='1', proof=100, gPointers={"1":1}, gIndex=1, previous_g_hash="1")#{"A":{"index":1,"hash":"233333"}}
# print(a)
# blockchain.submit_block(a)
# print(blockchain.last_block)
# print(blockchain.get_block_from_hash("2dcca01ab24e111bf8b006231c250a9e07e30c1df47ece8ba0defb15ce4075a9"))
# print(blockchain.get_gblock_from_index(1))

a = {"a":1}
blockchain.test(a)
print(a)

