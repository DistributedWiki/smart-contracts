from utils.utils import JSONSerializable


class Block(JSONSerializable):
    def __init__(self, timestamp=None, prevhash=None, transactions=None, proof=None, blk_number=0, difficulty=4):
        self.timestamp = timestamp
        self.prevhash = prevhash
        self.transactions = transactions or []
        self.proof = proof
        self.blk_number = blk_number
        self.difficulty = difficulty

    def add_transactions(self, transactions):
        self.transactions.extend(transactions)

    def verify(self):
        return self.hash()[:self.difficulty] == ''.join(['0'] * self.difficulty)
