from core.transaction import *


class Wallet(object):
    def __init__(self, address, chain, transactions_db):
        self.address = address
        self.chain = chain
        self.db = transactions_db

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
        output_recipient = TransactionOutput.create_unique_tx(recipient, value)
        outputs.append(output_recipient)

        if inputs_val > value + fee:
            output_change = TransactionOutput.create_unique_tx(self.address, inputs_val - value - fee)
            outputs.append(output_change)

        transaction = Transaction(inputs, outputs)
        transaction.sign("TODO")

        return transaction

    def send_transaction(self, recipient, value, fee):
        transaction = self.create_transaction(recipient, value, fee)

        #TODO - send

