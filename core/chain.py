class Chain(object):
    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        self.blocks.append(block)
        # TODO - send block and synchronize

    @property
    def last_block(self):
        return self.blocks[-1]

    def block_by_number(self, n):
        return self.blocks[n]
