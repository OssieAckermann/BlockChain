#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 18:49:31 2021

@author: Ossie Du
"""

import datetime
import hashlib
import json
from flask import Flask, jsonify

# Building a Block chain

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1,prev_hash = '0')
        
    def create_block(self, proof, prev_hash):
        block = {"index":len(self.chain)+1,
                 "timestamp":str(datetime.datetime.now()),
                 "proof":proof,
                 "prev_hash":prev_hash
        }
        self.chain.append(block)
        return block
        
    def get_prev_block(self):
        #return the lastest 
        return self.chain[-1]

    def proof_of_work(self,prev_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - prev_proof**2).encode()
            ).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dump(block, sort_key = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['prev_hash'] != self.hash(previous_block):
                return False
            
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2-previous_proof**2).encode()
            ).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

# Mining Block chain
app = Flask(__name__)

blockchain = Blockchain()
 
# Mining a new block
@app.route('/mine_block',methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_prev_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {"message":"Congratulation! you just mined a block!\n",
                "index":block['index'],
                "timestamp":block['timestamp'],
                "proof":block['proof'],
                "previous_hash":block['prev_hash']}
    return jsonify(response), 200
    
# Getting the full Blockchain
@app.route('/get_chain',methods = ['GET'])
def get_chain():
    response = {"chain":blockchain.chain,
                "length":len(blockchain.chain)}
    return jsonify(response), 200

# Running the app
app.run(host = '0.0.0.0',
        port = 5000)










