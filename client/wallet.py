from client.db import TransactionsDB
from core.transaction import *


class Wallet(object):
    def __init__(self, address, chain):
        self.address = address
        self.chain = chain
        self.db = TransactionsDB()

        # add all unspent transactions to db
        for block in self.chain.blocks:
            for transaction in block.transactions:
                if transaction.sender != BLOCK_REWARD:
                    for input in transaction.inputs:
                        self.db.remove(input.id)
                for output in transaction.outputs:
                    self.db.add(output)

    def create_transaction(self, recipient, value, fee):
        transactions = self.db.get_by_address(self.address)
        inputs = []
        inputs_val = 0

        for transaction in transactions:
            inputs.append(transaction.id)
            inputs_val += transaction.value

            if inputs_val >= value + fee:
                break

        outputs = []
        output_recipient = TransactionOutput(recipient, value)
        while self.db.exists(output_recipient.id):
            output_recipient.bump_nonce()

        outputs.append(output_recipient)

        if inputs_val > value + fee:
            output_change = TransactionOutput(self.address, inputs_val - value - fee)
            while self.db.exists(output_change.id):
                output_change.bump_nonce()

            outputs.append(output_change)

        transaction = Transaction(inputs, outputs)
        transaction.sign("TODO")

        return transaction

    def send_transaction(self, recipient, value, fee):
        transaction = self.create_transaction(recipient, value, fee)

        #TODO - send

