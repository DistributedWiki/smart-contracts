from core.chain import Chain
from network.node_manager import NodeManager, LAST_BLOCK


class Client(object):
    def __init__(self, known_peers):
        self.chain = self.__init_blockchain()
        self.node_manager = NodeManager(known_peers, self.chain, self.__new_block_handler)

    def update_chain(self):
        last_block = self.node_manager.request_block(LAST_BLOCK)
        last_block = last_block[0]  # TODO - check which block is valid

        for block_n in range(0, last_block):
            self.chain.add_block(self.node_manager.request_block(block_n))

    def __init_blockchain(self):
        return Chain()  # TODO - load from database/query other nodes

    def __new_block_handler(self, block):
        pass
