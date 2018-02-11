import time

from client.db import TransactionsDB
from core.block import Block
from core.transaction import Transaction
from utils.utils import JSONSerializable

block = Block(time.time(), 0, [])

while not block.verify_proof_of_work():
    block.nonce += 1

print(block.hash())
print(time.time() - block.timestamp)