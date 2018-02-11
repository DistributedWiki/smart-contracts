import queue

from time import *
from core.block import *
from core.transaction import *

TIME_FUTURE_THRESHOLD = 10 * 60


class Miner(object):
    def __init__(self, address, chain, transactions_db):
        self.address = address
        self.chain = chain
        self.db = transactions_db
        self.transactions_queue = queue.Queue()
        #TODO - register as node in network -> callback to transactions queue

    def get_transaction_input_value(self, transaction):
        inputs_value = 0
        for input_tid in transaction.inputs:
            inputs_value += self.db.get_by_tid(input_tid).value

        return inputs_value

    def validate_transaction(self, transaction):
        if not transaction.validate_signed():
            return False

        for input_tid in transaction.inputs:
            if input_tid != BLOCK_REWARD_ADDRESS and not self.db.exists(input_tid):
                return False

        # TODO - do not calculate this twice (in create block for fee calc)
        if self.get_transaction_input_value(transaction) < transaction.output_value:
            return False

        return True

    # TODO - where to put that - to Chain (synchornize problem)?
    def validate_block(self, block):
        """
        Checks if:
        - proof of work is valid
        - block timestamp, blk_number and prevhash are valid
        - there is only one reward
        - reward has correct value
        - all transactions are signed and valid
        """
        if not block.verify_proof_of_work():
            return False

        if block.timestamp > time() + TIME_FUTURE_THRESHOLD:
            return False

        prev_block = self.chain.block_by_number(block.blk_number - 1)
        if prev_block.timestamp >= block.timestamp:
            return False
        if prev_block.hash != block.prevhash:
            return False

        reward = 0
        available_fee = 0
        for tx in block.transactions:
            if not self.validate_transaction(tx):
                return False
            if tx.inputs[0] == BLOCK_REWARD_ADDRESS:
                if reward != 0:
                    return False
                else:
                    reward = tx.outputs[0].value
            else:
                available_fee += self.get_transaction_input_value(tx) - tx.output_value

        if reward != BLOCK_REWARD + available_fee:
            return False

        return True

    def create_block(self):
        transactions = []
        fee = 0
        while not self.transactions_queue.empty() and len(transactions) < BLOCK_TRANSACTIONS_N_LIMIT:
            t = self.transactions_queue.get()
            if self.validate_transaction(t):
                transactions.append(t)
                fee += self.get_transaction_input_value(t) - t.output_value
        # TODO - some algorithm for maximizing fees (implement in prorityQueue? )

        reward_transaction_out = TransactionOutput.create_unique_tx(self.address, BLOCK_REWARD + fee)
        reward_transaction = Transaction([BLOCK_REWARD_ADDRESS], reward_transaction_out)
        reward_transaction.sign("TODO")

        transactions.insert(0, reward_transaction)

        return Block(time(), self.chain.last_block.hash, transactions, self.chain.last_block.blk_number + 1)

    def mine_block(self, block):
        while not block.verify_proof_of_work():
            block.nonce += 1
        # TODO - interrupt when block is found by others
        return block

    def mine(self):
        block = self.create_block()
        block = self.mine_block(block)

        self.chain.add_block()




    # TODO
    # - synchronize with other blocks
