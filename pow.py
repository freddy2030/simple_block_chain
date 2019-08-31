# -*- coding: utf-8 -*-

import hashlib
import json
from time import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request, g, Flask,session

import levevdbapi
# import leveldb
import os
from blockchain import blockchain


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

@app.route('/setName', methods=['POST'])
def setName():
    values = request.form
    # print("@244",request.form.get('chainName'))
    name = values.get('chainName')
    if name:
        blockchain.setChainName(values["chainName"])
        response = {
            "status": "success",
            "message":"set name successed"
        } 
    else:
        response = {
            "status": "fail",
            "message":"set name failed"
        } 
    
    return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def mine():
    # 给工作量证明的节点提供奖励.
    # 发送者为 "0" 表明是新挖出的币
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # 生成候选区块
    index = len(blockchain.chain) + 1
    timestamp = time()
    current_transactions = blockchain.current_transactions
    last_block = blockchain.last_block
    previous_hash = blockchain.hash(last_block)

    block_tmp = blockchain.new_candidate_block(index,
                                               timestamp,
                                               current_transactions,
                                               previous_hash)

    # 完成工作量证明
    proof = blockchain.proof_of_work(block_tmp)
    block_hash = blockchain.get_hash_block_proof(block_tmp, proof)

    # 生成正式区块
    
    if block_hash[:4] == "0000":
        pinChain = json.load(open('./config/pinChain.json', 'r'))
        gPointer = []
        for pinName in pinChain:
            mhash = requests.get("http://%s/getLastHash" % pinChain[pinName][0])
            if mhash:
                # print(mhash.json()['hash'])
                gPointer.append(mhash.json()['hash'])
    
        print("xhxhxhxhxh",gPointer)
        block = blockchain.new_block(index, timestamp, current_transactions,
                                 previous_hash, proof, None)
        payload = json.dumps({"block":block})
        for pinName in pinChain:
            requests.post("http://%s/addGlobalBlock" % pinChain[pinName][0], data = payload)

        blockchain.globalchain.append(block)
        blockchain.globalchainindex += 1
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
                                 previous_hash, proof, None)
        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'hash': block_hash,
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
   
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
