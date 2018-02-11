from utils.utils import JSONSerializable

BLOCK_REWARD = 0


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

    def bump_nonce(self):
        self.nonce += 1

    @property
    def id(self):
        return self.hash()


class Transaction(JSONSerializable):
    def __init__(self, inputs=None, outputs=None):
        """

        :param inputs: list of transactions id's (OutputTransaction.id) to be spent
        :param outputs: list of OutTransaction objects
        """
        self.inputs = inputs or []
        self.outputs = outputs or []


    def validate(self):
        return "is signed - TODO"  # checking balance is not done here

    def sign(self, key):
        pass  #TODO

