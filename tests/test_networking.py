import pytest
import socket
import time

from airshare import Node, Connection


class TestConnection:
    def test_conn_init(self):
        ip = "127.0.0.1"
        port = 8888

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((ip, port))
        server.listen(2)
        server.setblocking(False)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((ip, port))
        server.accept()

        node = Node()
        conn = Connection(node, sock, "uid")
        assert conn.active and conn.raddr == (ip, port)

    def test_conn_stop(self):
        ip = "127.0.0.1"
        port = 8888

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((ip, port))
        server.listen(2)
        server.setblocking(False)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((ip, port))
        server.accept()

        node = Node()
        conn = Connection(node, sock, "uid")
        conn.stop()
        assert not conn.active


class TestNode:
    @pytest.mark.parametrize("ip", [None, "127.0.0.1"])
    @pytest.mark.parametrize("port", [None, 5555])
    def test_node_init(self, ip, port):
        node = Node(ip, port)
        assert node.active

    def test_node_stop(self):
        node = Node()
        node.stop()
        assert not node.active

    def test_node_connect_self(self):
        with pytest.raises(AssertionError):
            node = Node()
            node.connect_to_node(*node._addr)

    def test_node_connect_remote(self):
        node = Node()
        remote = Node()
        node.connect_to_node(*remote._addr)

    def test_node_connect_twice(self):
        with pytest.raises(AssertionError):
            node = Node()
            remote = Node()
            node.connect_to_node(*remote._addr)
            node.connect_to_node(*remote._addr)

    def test_node_destroy_connection(self):
        node = Node()
        remote = Node()
        node.connect_to_node(*remote._addr)
        node.stop()
        assert not node.connections

    def test_node_connect_multiple_remotes(self):
        node = Node()
        a = Node()
        b = Node()
        node.connect_to_node(*a._addr)
        node.connect_to_node(*b._addr)

    def test_node_destroy_all_connections(self):
        node = Node()
        a = Node()
        b = Node()
        node.connect_to_node(*a._addr)
        node.connect_to_node(*b._addr)
        node.stop()
        assert not node.connections

    def test_node_send_remote(self):
        node = Node()
        remote = Node()
        node.connect_to_node(*remote._addr)
        node.send(node.connections[0], "airshare")
        time.sleep(1)
        assert remote.data == "airshare"

    def test_node_send_all(self):
        node = Node()
        a = Node()
        b = Node()
        node.connect_to_node(*a._addr)
        node.connect_to_node(*b._addr)
        node.send_all("airshare")
        time.sleep(1)
        assert a.data == "airshare" and b.data == "airshare"
