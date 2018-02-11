from utils.utils import JSONSerializable

BLOCK_TRANSACTIONS_N_LIMIT = 1000
BLOCK_REWARD = 25


class Block(JSONSerializable):
    def __init__(self, timestamp=None, prevhash=None, transactions=None, blk_number=0, nonce=0, difficulty=4):
        self.timestamp = timestamp
        self.prevhash = prevhash
        self.transactions = transactions or []
        self.nonce = nonce
        self.blk_number = blk_number
        self.difficulty = difficulty

    def add_transactions(self, transactions):
        self.transactions.extend(transactions)

    def verify_proof_of_work(self):
        return self.hash()[:self.difficulty] == ''.join(['0'] * self.difficulty)
