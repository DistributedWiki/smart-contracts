import queue

from time import *
from core.block import *


TIME_FUTURE_THRESHOLD = 10 * 60


class Miner(object):
    def __init__(self, address, chain):
        self.address = address
        self.chain = chain
        self.transactions_queue = queue.Queue()
        #TODO - register as node in network -> callback to transactions queue

    def validate_transaction(self, transaction):
        return True

    def create_block(self):
        transactions = []
        while not self.transactions_queue.empty() and len(transactions) < BLOCK_TRANSACTIONS_N_LIMIT:
            t = self.transactions_queue.get()
            if self.validate_transaction(t):
                transactions.append(t)

        return Block(time(), self.chain.last_block.hash, transactions, self.chain.last_block.blk_number + 1)

    def mine_block(self, block):
        while not block.verify_proof_of_work():
            block.nonce += 1
        # TODO - interrupt when block is found by others
        return block

    def mine(self):
        block = self.create_block()
        block = self.mine_block(block)

        self.chain.add_block()




    # TODO
    # - synchronize with other blocks
