class WrongBlockException(Exception):
    pass

class Chain(object):
    def __init__(self):
        self.blocks = []  # blocks which are known for sure to be on the chain
        self.heads = []  # heads of chains with the same length (when 2, or more miners send different valid blocks)
        self.branch_n = 0  # number of last block known to be in chain (after this blocks few branches may exist)

        self.heads[0] = self.blocks  # self.heads have at least one element -> head of valid blockchain

    def add_block(self, block):
        # consensus:
        #
        #    123456789
        # 1.        ##
        #          /
        # 2. ######   ##
        #          \ /
        #           #
        #            \
        # 3.          #

        # we must keep all branches until one is signigicantly longer (TODO - 2 blocks or hiperparameter???), then we may
        # remove others



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
        return self.heads[0][-1]  # last element of one of the branches (possibly there is only one branch)

    def block_by_number(self, n):
        if n <= self.branch_n:
            return self.blocks[n]
        else:
            return self.heads[0][n - self.branch_n]
