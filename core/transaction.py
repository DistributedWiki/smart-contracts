from utils.utils import JSONSerializable

BLOCK_REWARD_ADDRESS = 0


class TransactionOutput(JSONSerializable):
    def __init__(self, recipient=None, value=None, nonce=0):
        """

        :param recipient: recipient of the transaction
        :param value: value to be transferred
        :param nonce: used as countermeasure for id (hash) collision,
               if it turns out that transaction hash is the same as one of transactions
               already in blockchain this value can be modified
        """
        self.recipient = recipient
        self.value = value
        self.nonce = nonce

    @property
    def id(self):
        return self.hash()

    @staticmethod
    def create_unique_tx(recipient, value, transactions_db):
        t = TransactionOutput(recipient, value)
        while transactions_db.exists(t.id):
                t.nonce += 1
        return t


class Transaction(JSONSerializable):
    def __init__(self, inputs=None, outputs=None):
        """

        :param inputs: list of transactions id's (TransactionOutput.id) to be spent
        :param outputs: list of TransactionOutput objects
        """
        self.inputs = inputs or []
        self.outputs = outputs or []

    @property
    def output_value(self):
        v = 0
        for output_tx in self.outputs:
            v += output_tx.value
        return v

    def validate_signed(self):
        return "is signed - TODO"

    def sign(self, key):
        pass  #TODO

