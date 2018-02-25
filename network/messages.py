from utils.utils import JSONSerializable

LAST_BLOCK = -1


class MessageDiscover(JSONSerializable):
    pass


class MessageDiscoverResponse(JSONSerializable):
    def __init__(self, peers):
        self.peers = peers


class MessageRequestBlock(JSONSerializable):
    def __init__(self, block_n):
        self.block_n = block_n


class MessageSendBlock(JSONSerializable):
    def __init__(self, block):
        self.block = block


class MessageSendTransaction(JSONSerializable):
    def __init__(self, transaction):
        self.transaction = transaction
