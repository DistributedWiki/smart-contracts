class Chain(object):
    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        self.blocks.append(block)

    def validate_block(self, block):
        """
        Checks if:
        - proof of work is valid
        - block timestamp, blk_number and prevhash are valid
        """
        if not block.verify_proof_of_work():
            return False

        if self.blocks:  # if not first block
            prev_block = self.blocks[block.blk_number - 1]
            if prev_block.timestamp >= block.timestamp:
                return False
            if prev_block.hash != block.prevhash:
                return False

        return True

    @property
    def last_block(self):
        return self.blocks[-1]

    def block_by_number(self, n):
        return self.blocks[n]
