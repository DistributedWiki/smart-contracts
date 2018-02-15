from utils.utils import JSONSerializable


class Transaction(JSONSerializable):
    def __init__(self, data=None, nonce=0):
        self.data = data
        self.nonce = nonce

    @property
    def id(self):
        return self.hash()

