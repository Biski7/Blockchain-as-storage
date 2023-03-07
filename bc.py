import hashlib
import time
from datetime import datetime
from pprint import pprint
import sys 
import csv
import psutil
import os 

# Generate the hash of any given input
def hashGenerator(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Generate the hash of a file
def hashGeneratorfile(data):
    with open(data, 'rb') as f: 
        fb = f.read() 
        file_hash = hashlib.sha256(fb)
    return [file_hash.hexdigest(), fb]

class Blockchain(object):
    def __init__(self):
        self.chain = []
        index = 0
        hashLast = None
        timestamp = datetime.now()
        hashStart = hashGenerator( hashGenerator('gen_hash') + hashGenerator(str(index)) + hashGenerator(str(timestamp)))
        genesis_block = {
            'index': index,
            'data': 'gen_hash',
            'timestamp': timestamp,
            'hash_of_current_block': hashStart,
            'hash_of_previous_block': hashLast,
        }
        self.chain = [genesis_block]
    
    def add_block(self, file_name):
        # starttime = time.monotonic()
        starttime = time.time_ns()
        index = len(self.chain)
        timestamp = datetime.now()
        hash_of_previous_block = self.chain[-1]['hash_of_current_block']
    
        hash_of_current_block = 0
        data_hash, data = hashGeneratorfile(file_name)
        hash_string = str(timestamp).join([str(index), hash_of_previous_block,data_hash])
        hash_of_current_block = hashGenerator(hash_string)
        
        block = {
            'index': index,
            'data': data,
            'timestamp': timestamp,
            'hash_of_current_block': hash_of_current_block,
            'hash_of_previous_block': hash_of_previous_block
        }

        # add the new block to the blockchain
        if self.valid_chain(self.chain) == False:
            return False
        self.chain.append(block) 
        # endtime = time.monotonic()
        endtime = time.time_ns()
        size = sys.getsizeof(block)
        elapsed_time = endtime - starttime

        with open('log.csv', 'a') as csvf:
            writer = csv.writer(csvf, dialect= csv.excel)
            writer.writerow([index, elapsed_time, size])

        return block
    
    # determine if a given blockchain is valid
    def valid_chain(self, chain):
        current_index = 1 # starts with the second block
        previous_index = 0
        
        while current_index < len(chain):
            block = chain[current_index]
            block_previous = chain[previous_index]
            if block['hash_of_previous_block'] != block_previous['hash_of_current_block']:
                return False
            # move on to the next block on the chain
            current_index += 1
            previous_index += 1
        return True


with open('log.csv', 'a') as csvf:
    writer = csv.writer(csvf, dialect= csv.excel)
    writer.writerow(['index', 'elapsed_time', 'size'])

bc = Blockchain()


## The argument given in the command line will server as the number of blocks
## eg. python bc.py 5 gives 5 blocks not including genesis block
number_of_blocks = int(sys.argv[1])

n = 1
while n <= number_of_blocks:
    # Including the name of the file to be stored in BC
    file = 'test.uxp'
    bc.add_block(file)
    n += 1
    
# Printing out the blocks 
for block in bc.chain:
    ## To print out whole block use the code below 
    # pprint(block)

    # print everything except the data stored
    index = block['index']
    timestamp = block['timestamp']
    current_hash = block['hash_of_current_block']
    previous_hash = block['hash_of_previous_block']
    print(f'Index: {index}')
    print(f'Timestamp: {timestamp}')
    print(f'Current Hash: {current_hash}')
    print(f'Previous Hash: {previous_hash}')
    print("\n")

