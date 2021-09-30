import random
import string
import time

from airshare import Node
from airshare import Clipboard
from pyperclip import copy


def random_str(length):
    return "".join(random.sample(string.ascii_letters + string.digits, length))


class TestClipboard:
    def test_cpb_init(self):
        node = Node()
        clipboard = Clipboard(node)
        assert clipboard.active

    def test_cpb_simple(self):
        data = random_str(length=20)
        copy(data)
        clipboard = Clipboard(Node())
        assert clipboard.cpb == data

    def test_cpb_without_remote(self):
        data = random_str(length=20)
        copy("")
        clipboard = Clipboard(Node())
        copy(data)
        assert not clipboard.cpb

    def test_cpb_with_remote(self):
        data = random_str(length=20)
        a = Node()
        b = Node()
        a.connect_to_node(*b._addr)
        clipboard = Clipboard(a)
        copy(data)
        time.sleep(2)
        assert clipboard.cpb == data and a.data == data and b.data == data
