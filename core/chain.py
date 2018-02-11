class Chain(object):
    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        self.blocks.append(block)
        pass

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    def last_block(self):
        return self.blocks[-1]

    def block_by_number(self, n):
        return self.blocks[n]
