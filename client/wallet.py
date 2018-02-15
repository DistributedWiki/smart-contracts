from core.transaction import *


class Wallet(object):
    def __init__(self, address, chain):
        self.address = address
        self.chain = chain

    def create_transaction(self, data):
        return Transaction(data)

    def send_transaction(self, data):
        transaction = self.create_transaction(data)

        #TODO - send

