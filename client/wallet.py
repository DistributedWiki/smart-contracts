from client.client import Client
from core.transaction import *


class Wallet(Client):
    def send_transaction(self, data):
        t = Transaction(data)
        self.node_manager.broadcast_transaction(t)

