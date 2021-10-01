"""
This implements classes for Nodes and Connections in a peer-to-peer networking
scheme. 

Each Node is a server and a client. Nodes can connect to other Nodes and send
and receive information.
"""

import logging
import socket

from hashlib import sha1
from threading import Thread

socket.setdefaulttimeout(1)
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)


class Connection(Thread):
    def __init__(self, node, sock, conn_node_id):
        super(Connection, self).__init__()
        self.node = node
        self.sock = sock
        self.laddr = sock.getsockname()
        self.raddr = sock.getpeername()
        self.conn_node_id = conn_node_id
        self.active = False
        self.start()

    def run(self):
        self.active = True

        while self.active:
            try:
                data = self.sock.recv(8192)

                if data:
                    self.node.data = data.decode()
                else:
                    logging.info(
                        f"Connection to {self.laddr[0]}:{self.laddr[1]} was lost"
                    )
                    self.stop()

            except socket.timeout:
                pass

    def send(self, msg):
        self.sock.sendall(str(msg).encode())

    def stop(self):
        if self.active:
            self.active = False
            self.node.disconnect_connection(self)

    def __str__(self):
        return f"<Connection raddr={self.raddr[0]}:{self.raddr[1]}>"

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.node)}, {self.sock}, {self.conn_node_id})"


class Node(Thread):
    def __init__(self, host=None, port=None):
        super(Node, self).__init__()
        self.init_server(host, port)
        self.id = sha1(self.addr.encode()).hexdigest()
        self.active = False
        self.connections = []
        self.data = ""
        self.start()

        logging.info(f"Node started {self._addr}")

    @property
    def addr(self):
        return f"{self._addr[0]}:{self._addr[1]}"

    def init_server(self, host, port):
        self.hostname = socket.gethostname()
        self.host = str(host) if host else socket.gethostbyname(self.hostname)
        self.port = int(port) if port else 0

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))

        self._addr = self.server.getsockname()

        self.server.listen()

    def unbind_server(self):
        self.server.close()

    def accept_node(self):
        conn, _ = self.server.accept()
        conn_node_id = conn.recv(8192).decode()
        conn.send(self.id.encode())

        self.create_connection(conn, conn_node_id)

        logging.info(f"Connected by: {conn_node_id}")

    def run(self):
        self.active = True

        while self.active:
            try:
                self.accept_node()

            except socket.timeout:
                pass

    def stop(self):
        if self.active:
            self.active = False
            self.disconnect_all()
            self.unbind_server()

    def connect_to_node(self, host, port):
        host, port = str(host), int(port)
        if not self.active:
            raise AssertionError("Node is stopped.")

        elif (host, port) == self._addr:
            raise AssertionError("Cannot connect to self.")

        elif any([(host, port) == c.raddr for c in self.connections]):
            raise AssertionError("Peer is already connected.")

        else:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.connect((host, port))
                sock.send(self.id.encode())
                conn_node_id = sock.recv(4096).decode()

                self.create_connection(sock, conn_node_id)

                logging.info(f"Connected to: {conn_node_id}")

            except Exception as e:
                logging.error(e)

    def create_connection(self, sock, conn_node_id):
        connection = Connection(self, sock, conn_node_id)
        self.connections.append(connection)

    def disconnect_connection(self, connection):
        if connection in self.connections:
            self.connections.pop(self.connections.index(connection))
            connection.stop()

    def disconnect_all(self):
        while self.connections:
            self.disconnect_connection(self.connections[0])

    def send(self, connection, msg):
        connection.send(msg)

    def send_all(self, msg):
        for c in self.connections:
            self.send(c, msg)

    def __str__(self):
        return f"<Node server={self.addr}, active={self.active}, conns={self.connections}, id={self.id}>"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._addr[0]}', {self._addr[1]})"
