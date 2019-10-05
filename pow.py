# -*- coding: utf-8 -*-

import hashlib
import json
from time import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request, g, Flask,session

# import levevdbapi
# import leveldb
import os
from blockchain import blockchain
import util

# Instantiate the Node
app = Flask(__name__)
# app.config['SECRET_KEY'] = os.urandom(24)
# print(id(blockchain))
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
# db = levevdbapi.LevelDB()

# if db not in g:
#     g.db = levevdbapi.LevelDB()


# if 'username' not in session:
   
    # session['username'] = 'liefyuan'

@app.route('/')
def hello_world():
    # print(session.get("11111111"))
    # if not session.get("blockchain"):
    #     session['blockchain'] = Blockchain(levevdbapi.LevelDB())
    # g.a = "111"
    # session["a"] = {"a":1}
    return 'Hello, this is your first blockchain!' 

@app.route('/test')
def test():
    # return str(session.get('a')["a"])
    # a = app.app_context()
    # a.push()
    print(g.a)
    return "haha"

@app.route('/getLastHash', methods=['GET'])
def get_last_hash(): 
    response = {
        "hash": blockchain.hash(blockchain.last_block)
    }   
    return jsonify(response), 200
@app.route("/get_all_account", methods=['GET'])
def get_all_account():
    AllaccountList = {}
    # print(blockchain.account)
    # for account in blockchain.account:
    #     accountList[account] = blockchain.db.getValue(account)
    accountList = blockchain.db.getValue("account-list")
    if accountList:
        for account in accountList["data"]:
            AllaccountList[account] = blockchain.db.getValue(account)
    return jsonify(AllaccountList), 200

@app.route('/get_all_info', methods=['GET'])
def get_all_info():
    i = 0
    blockList = {}
    while( i <= blockchain.index):
        blockInfo = blockchain.get_block_info_from_index(str(i))
        for blockHash in blockInfo["blockpool"]:
            blockInfo[blockHash] = blockchain.get_block_with_transcation_from_hash(blockHash)
        blockList["block-"+str(i)] = blockInfo
        i+=1
    return jsonify(blockList), 200
@app.route('/mine', methods=['GET'])
def mine():
    # 给工作量证明的节点提供奖励.
    # 发送者为 "0" 表明是新挖出的币
    # blockchain.new_transaction(
    #     sender="0",
    #     recipient=node_identifier,
    #     amount=1,
    # )

    # 生成候选区块
    index = blockchain.index + 1
    gindex = blockchain.globalchainindex + 1
    timestamp = time()
    current_transactions = blockchain.get_transactions_pool()
   
    last_block = blockchain.last_block
    print("1111111")
    print(last_block)
    previous_hash = util.hash( last_block )

    last_g_block = blockchain.last_gblock
    # previous_g_hash = blockchain.hash( last_g_block )
    previous_g_hash = "4f025c4ef95f64c069dc448b3aef548332f0db12ef7567ff8fa345bd16fe8f11"
    
    block_tmp = blockchain.new_candidate_block(index,
                                               timestamp,
                                               current_transactions,
                                               previous_hash, gIndex = gindex, previous_g_hash = previous_g_hash)

    # 完成工作量证明
    proof = blockchain.proof_of_work(block_tmp)
    block_hash = blockchain.get_hash_block_proof(block_tmp, proof)

    # 生成正式区块
    
    if block_hash[:4] == "0000000":
        pinChain = json.load(open('./config/pinChain.json', 'r'))
        gPointer = []
        for pinName in pinChain:
            mhash = requests.get("http://%s/getLastHash" % pinChain[pinName][0])
            if mhash:
                # print(mhash.json()['hash'])
                gPointer.append(mhash.json()['hash'])
    
        # print("xhxhxhxhxh",gPointer)
        block = blockchain.new_block(index, timestamp, current_transactions,
                                 previous_hash, proof, None)
        payload = json.dumps({"block":block})
        for pinName in pinChain:
            requests.post("http://%s/addGlobalBlock" % pinChain[pinName][0], data = payload)

        blockchain.submit_global_block( block )
        # blockchain.globalchainindex += 1
        response = {
            'message': "New Global Block",
            'index': block['index'],
            'hash': block_hash,
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
            'gPointer': gPointer,
            'gindex': blockchain.globalchainindex
        }
    else :
        block = blockchain.new_block(index, timestamp, current_transactions,
                                 previous_hash, proof, previous_g_hash, gIndex=gindex)
        print(block)
        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'hash': block_hash,
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        if len(blockchain.transactionList) == 0:
            print("11111")
            blockchain.transactionList.append(util.getMinerTranscation("776b95dc71eff9c4ecf5762c46acebdad73e73de"))
        blockchain.submit_block(block, blockchain.transactionList)
        blockchain.transactionList.clear()
        blockchain.transactionList.append(util.getMinerTranscation("776b95dc71eff9c4ecf5762c46acebdad73e73de"))
    
   
    return jsonify(response), 200

@app.route('/addGlobalBlock', methods=['POST'])
def addGlobalBlock():
    values = request.data
    gblock = json.loads(values.decode('utf-8'))['block']
    print(gblock)
    blockchain.globalchain.append(gblock)
    if(gblock['gindex'] > blockchain.globalchainindex):
        blockchain.globalchainindex = gblock['gindex']
    response = {
        "message": gblock
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.form

    # Create a new Transaction
    index = blockchain.new_transaction(
        values['sender'], values['recipient'], values['amount'])

    # response = {'message': f'Transaction will be added to Block {index}'}
    response = {'message': 'Transaction will be added to Block %s' % (index)}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        "chainName": blockchain.chainName,
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
        'global': blockchain.globalchain 
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.form.to_dict()
    # if nodes is None:
    #     return "Error: Please supply a valid list of nodes", 400

    for n, ip in values.items():
        blockchain.register_node(ip)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-c', '--config', default='default',
                        type=str, help='ipconfig')

    args = parser.parse_args()

    config = json.load(open('./config/' + args.config+'.json', 'r'))
    ip = config['ip']
    port = config['port']
    # print("1111111111111111111")
    # db = leveldb.LevelDB('./db')
    # app.app_context().push()
    # app.config['SECRET_KEY'] = os.urandom(24)
    app.run(host=ip, port=port,debug=True)
