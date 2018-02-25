import threading
from time import *

from client.client import Client
from core.block import *


TIME_FUTURE_THRESHOLD = 10 * 60


class Miner(Client):

    def __init__(self, known_peers):
        super().__init__(known_peers)
        self.new_block_event = threading.Event()
        self.new_block_event.clear()

    def validate_transaction(self, transaction):
        return True

    def create_block(self):
        transactions = []
        while not self.node_manager.pending_transactions and len(transactions) < BLOCK_TRANSACTIONS_N_LIMIT:
            t = self.node_manager.pending_transactions.get()
            if self.validate_transaction(t):
                transactions.append(t)

        return Block(time(), self.chain.last_block.hash, transactions, self.chain.last_block.blk_number + 1)

    def mine_block(self, block):
        while not block.verify_proof_of_work() and not self.new_block_event.is_set():
            block.nonce += 1

        return block

    def mine(self):
        block = self.create_block()
        block = self.mine_block(block)

        self.chain.add_block(block)
        self.node_manager.broadcast_block(block)

    def __new_block_handler(self, block):
        self.new_block_event.set()
        self.chain.add_block(block)


