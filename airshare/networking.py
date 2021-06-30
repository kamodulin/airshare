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
        self.active = True
        self.start()

    def run(self):
        while self.active:
            try:
                data = self.sock.recv(4096)

                if data:
                    self.node.data = data.decode()

                else:
                    self.node.disconnect_connection(self)
                    logging.info(f"Connection to {self.laddr[0]}:{self.laddr[1]} was lost")

            except socket.timeout:
                pass

            except Exception as e:
                self.node.disconnect_connection(self)
                logging.error(e)

        self.sock.close()

    # encryption
    def send(self, msg):
        self.sock.sendall(str(msg).encode())

    def stop(self):
        if self.active:
            self.active = False
        else:
            logging.warning("Connection is already stopped.")

    def __repr__(self):
        return f"<Connection raddr={self.raddr[0]}:{self.raddr[1]}>"


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
        self.host = host if host else socket.gethostbyname(self.hostname)
        self.port = port if port else 0

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))

        self._addr = self.server.getsockname()

        self.server.listen(1)

    def unbind_server(self):
        self.server.close()

    def accept_node(self):
        conn, addr = self.server.accept()
        conn_node_id = conn.recv(4096).decode()
        conn.send(self.id.encode())

        connection = self.create_connection(conn, conn_node_id)

        logging.info(f"Connected by: {conn_node_id}")

    def run(self):
        self.active = True

        while self.active:
            try:
                self.accept_node()

            except socket.timeout:
                pass

            except Exception as e:
                self.stop()
                logging.error(e)

        self.stop()

    def stop(self):
        if self.active:
            self.active = False
            
            self.disconnect_all()
            self.unbind_server()

        else:
            logging.warning("Node has already stopped.")

    def connect_to_node(self, host, port):
        if (host, port) == self._addr:
            logging.error("Cannot connect to self.")

        elif any([(host, port) == c.raddr for c in self.connections]):
            logging.error("Peer is already connected.")

        else:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.connect((host, port))
                sock.send(self.id.encode())
                conn_node_id = sock.recv(4096).decode()

                connection = self.create_connection(sock, conn_node_id)

                logging.info(f"Connected to: {conn_node_id}")

            except Exception as e:
                logging.error(e)

    def create_connection(self, sock, conn_node_id):
        connection = Connection(self, sock, conn_node_id)
        self.connections.append(connection)

    def disconnect_connection(self, connection):
        connection.stop()
        del self.connections[self.connections.index(connection)]

    def disconnect_all(self):
        for c in self.connections:
            self.disconnect_connection(c)

    def send(self, connection, msg):
        connection.send(msg)

    def send_all(self, msg):
        for c in self.connections:
            self.send(c, msg)

    def __repr__(self):
        return f"<Node server={self.addr}, active={self.active}, conns={self.connections}, id={self.id}>"