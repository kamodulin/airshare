import pytest
import random
import string
import time

from airshare import Node


def create_nodes(num, ip=None, port=None):
    if num == 1:
        return Node(ip, port)
    return [Node() for _ in range(num)]


def stop(*args):
    for node in args:
        if node.active:
            node.stop()


@pytest.mark.parametrize("ip", [None, "127.0.0.1"])
@pytest.mark.parametrize("port", [None, 5555])
def test_node_init(ip, port):
    node = create_nodes(1, ip, port)
    assert node.active
    stop(node)


def test_node_stop():
    node = create_nodes(1)
    stop(node)
    assert not node.active


def test_node_connect_self():
    with pytest.raises(AssertionError):
        node = create_nodes(1)
        node.connect_to_node(*node._addr)
    stop(node)


def test_node_connect_remote():
    nodes = p1, p2 = create_nodes(2)
    p1.connect_to_node(*p2._addr)
    stop(*nodes)


def test_node_connect_after_stopped():
    nodes = p1, p2 = create_nodes(2)
    p1.stop()
    with pytest.raises(AssertionError):
        p1.connect_to_node(*p2._addr)
    stop(*nodes)


def test_node_bidrectional():
    nodes = p1, p2 = create_nodes(2)
    p1.connect_to_node(*p2._addr)
    p2.connect_to_node(*p1._addr)
    stop(*nodes)


def test_node_connect_twice():
    with pytest.raises(AssertionError):
        nodes = create_nodes(2)
        for _ in range(2):
            nodes[0].connect_to_node(*nodes[1]._addr)
    stop(*nodes)


def test_node_destroy_connection():
    nodes = p1, p2 = create_nodes(2)
    p1.connect_to_node(*p2._addr)
    p1.stop()
    time.sleep(2)
    assert not p1.connections and not p2.connections
    stop(*nodes)


def test_node_connect_multiple_remotes():
    nodes = p1, p2, p3 = create_nodes(3)
    p1.connect_to_node(*p2._addr)
    p1.connect_to_node(*p3._addr)
    stop(*nodes)


def test_node_destroy_all_connections():
    nodes = p1, p2, p3 = create_nodes(3)
    p1.stop()
    assert not p1.connections and not p2.connections and not p3.connections
    stop(*nodes)


def test_node_send_remote():
    nodes = p1, p2 = create_nodes(2)
    data = "".join(random.sample(string.ascii_letters + string.digits, 20))
    p1.connect_to_node(*p2._addr)
    p1.send(p1.connections[0], data)
    time.sleep(1)
    assert p2.data == data
    stop(*nodes)


def test_node_send_all():
    nodes = p1, *peers = create_nodes(4)
    data = "".join(random.sample(string.ascii_letters + string.digits, 20))
    for peer in peers:
        p1.connect_to_node(*peer._addr)
    p1.send_all(data)
    time.sleep(1)
    for peer in peers:
        assert peer.data == data
    stop(*nodes)
