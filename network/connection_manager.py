import queue
import socket
import threading
import select

BUFFER_SIZE = 1024
ALL_PEERS = "ALL_PEERS"


class ConnectionManager(object):
    def __init__(self,
                 address,
                 port,
                 message_handler=lambda p, m: print(m.decode),
                 new_connection_handler=lambda p: None,
                 close_connection_handler=lambda p: None):
        """
        :param address: address of this host
        :param port: port on which we will listen
        :param message_handler: callback to handle messages from peers: callback(peer, message)
        :param new_connection_handler: callback to handle new connections from peers: callback(peer_address)
        :param close_connection_handler: callback to handle closing connection by peer: callback(peer_address)
        """
        self.address = address
        self.port = port
        self.message_handler = message_handler
        self.new_connection_handler = new_connection_handler
        self.close_connection_handler = close_connection_handler

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setblocking(0)
        self.server_socket.bind((self.address, port))
        self.server_socket.listen()

        # This list holds refs to all sockets from which we could read
        self.inputs = [self.server_socket]  # TODO multithreaded get/insert?

        # This list holds ref to all sockets to which we could write
        self.outputs = []

        # Dict { 'socket' : Queue } where 'Queue' holds messages to be sent to 'socket'
        self.message_queues = {}

        # Dict { 'peer address' : socket }
        self.peers_connections = {}

        self.main_thread = None
        self.running = False

    @property
    def peers(self):
        return self.inputs[1:]  # peers = all sockets except server_socket

    def connect(self, peer):
        """
        :param peer: address of a peer as tuple: (address, port)
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(peer)

        self.inputs.append(sock)
        self.message_queues[sock] = queue.Queue()
        self.peers_connections[peer] = sock

    def __send_message(self, peer, message):
        connection = self.peers_connections[peer]
        self.message_queues[connection].put_nowait(message)
        if connection not in self.outputs:
            self.outputs.append(connection)

    def send_message(self, peer, message):
        """
        Sends message asynchronously to a peer (connection must have been established first):
        either by calling connect(peer) OR by remote host

        :param peer: address of a peer as tuple: (address, port)
        :param message: encoded message (in binary format)
        """
        if peer == ALL_PEERS:
            for p in self.peers:
                self.__send_message(p, message)
        else:
            self.__send_message(peer, message)

    def start_main_thread(self):
        """
        Starts main thread which is responsible for accepting new connections, as well as receiving and sending data
        """
        self.running = True
        self.main_thread = threading.Thread(target=self.__start)
        self.main_thread.start()

    def stop_main_thread(self):
        self.running = False
        self.main_thread.join()

    def __start(self):
        while self.inputs and self.running:
            readable, writeable, errored = select.select(self.inputs, self.outputs, self.inputs, 1)
            # there is 1 s timeout because we can concurrently modify self.outputs (by calling send message)
            # without that timeout we could not add new sockets to self.outputs until select returns

            for s in readable:
                if s is self.server_socket:  # accept new connection
                    connection, _ = s.accept()
                    connection.setblocking(0)
                    self.inputs.append(connection)
                    self.message_queues[connection] = queue.Queue()
                    self.new_connection_handler(connection.getpeername())
                else:  # receive data
                    data = s.recv(BUFFER_SIZE)
                    if data:
                        self.message_handler(s.getpeername(), data)
                    else:  # if data is 0, it means that connection has been closed by remote host
                        self.inputs.remove(s)
                        del self.message_queues[s]
                        s.close()
                        self.close_connection_handler(s.getpeername())

            for w in writeable:
                try:  # for every ready socket, send message from queue (if there is any)
                    next_msg = self.message_queues[w].get_nowait()
                    w.send(next_msg)
                except queue.Empty:  # if there is no message in queue - remove socket from outputs list
                    self.outputs.remove(w)

            for e in errored:
                self.inputs.remove(e)
                if e in self.outputs:
                    self.outputs.remove(e)
                e.close()
                self.close_connection_handler(e.getpeername())
                del self.message_queues[e]

