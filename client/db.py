from core.transaction import *


class TransactionsDB(object):
    """
    This class servers as database to hold all unspent transactions (of all nodes).
    It is used to verify that transaction is valid (inputs of transaction has not been spent).
    """
    def __init__(self, chain):
        self.data = dict()
        self.chain = chain

        # add all unspent transactions to db
        for block in self.chain.blocks:
            for transaction in block.transactions:
                if transaction.sender != BLOCK_REWARD_ADDRESS:
                    for input in transaction.inputs:
                        self.remove(input.id)
                for output in transaction.outputs:
                    self.add(output)

    def add(self, t):
        self.data[t.id] = t

    def remove(self, tid):
        self.data.pop(tid)

    def get_by_tid(self, tid):
        return self.data[tid]

    def get_by_address(self, address):
        """
        get unspent output transactions whose recipient was 'address'
        """
        transactions = []
        for d in self.data:
            if d.recipient == address:
                transactions.append(d)

        return transactions

    def exists(self, tid):
        return tid in self.data