from network.connection_manager import *
from network.messages import *


class NodeManager(object):
    def __init__(self, known_peers, chain, new_block_handler):
        """
        Connects to all know_peers and accepts all new connections -> keep connection to every alive node
        :param known_peers: list of know peers
        :param chain: local blockchain
        :param new_block_handler: callback function for receiving new block
        """
        self.__pending_transactions = queue.Queue()
        self.awaiting_block = threading.Event()
        self.awaiting_block_list = []
        self.awaiting_block_number = None

        self.peers = []
        self.chain = chain
        self.new_block_handler = new_block_handler

        self.connection_manager = ConnectionManager('',
                                                    1234,
                                                    self.__handle_message,
                                                    self.__handle_new_connection,
                                                    self.__handle_close_connection)

        self.connection_manager.start_main_thread()
        self.__connect_to_peers(known_peers)

        if not self.peers:
            raise Exception("all peers unreachable")

        for peer in self.peers:
            self.connection_manager.send_message(peer, MessageDiscover().serialize())

    def broadcast_transaction(self, transaction):
        for peer in self.peers:
            self.connection_manager.send_message(peer, MessageSendTransaction(transaction).serialize())

    def broadcast_block(self, block):
        for peer in self.peers:
            self.connection_manager.send_message(peer, MessageSendBlock(block).serialize())

    def request_block(self, block_number):
        """
        Sends request to all known nodes and waits for response (from all nodes or until timeout)

        :param block_number: number of requested block
        :return: list of block returned by peers (in case they were different)
        """
        for peer in self.peers:
            self.connection_manager.send_message(peer, MessageRequestBlock(block_number).serialize())

        self.awaiting_block_number = block_number
        self.awaiting_block_list.clear()
        self.awaiting_block.clear()
        self.awaiting_block.wait(timeout=5)

        return self.awaiting_block_list

    @property
    def pending_transactions(self):
        txs = self.__pending_transactions
        self.__pending_transactions = queue.Queue()  # clear transactions

        return txs

    def __handle_message(self, peer, data):
        message = JSONSerializable.deserialize(data)
        response = None

        if message is MessageDiscover:
            response = MessageDiscoverResponse(self.peers)  # give info about all known peers
        elif message is MessageDiscoverResponse:
            self.__connect_to_peers(message.peers)
        elif message is MessageRequestBlock:
            if message.block_n == LAST_BLOCK:
                response = MessageSendBlock(self.chain.last_block)
            else:
                response = MessageSendBlock(self.chain.block_by_number(message.block_n))
        elif message is MessageSendBlock:
            if not self.awaiting_block.is_set() and message.block.blk_number == self.awaiting_block_number:
                self.awaiting_block_list.append(message.block)
                if len(self.awaiting_block_list) == len(self.peers):  # if all peers replied
                    self.awaiting_block.set()
            else:
                self.new_block_handler(message.block)
        elif message is MessageSendTransaction:
            self.__pending_transactions.put(message.transaction)

        if response is not None:
            self.connection_manager.send_message(peer, response.serialize())

    def __connect_to_peers(self, peers):
        for peer in peers:
            try:
                self.connection_manager.connect(peer)
            except Exception:
                pass
            else:
                self.peers.append(peer)

    def __handle_new_connection(self, peer):
        self.peers.append(peer)

    def __handle_close_connection(self, peer):
        self.peers.remove(peer)
