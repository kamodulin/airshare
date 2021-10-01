import argparse
import time

from airshare.networking import Node
from pyperclip import copy, paste
from threading import Thread


class Session(Thread):
    def __init__(self, host=None, remote=None):
        super(Session, self).__init__()
        self.host = host
        self.remote = remote
        self.node = self.init_node()
        self.log = {}

        if self.remote:
            remote = self.remote.split(":")
            self.node.connect_to_node(remote[0], remote[1])

        self.start()

    def init_node(self):
        if self.host:
            host = self.host.split(":")
            return Node(host[0], host[1])

        node = Node()
        self.host = node.addr
        return node

    def run(self):
        self.active = True
        self.clipboard = paste()
        while self.active:
            try:
                if self.node.connections:
                    tmp = paste()
                    if tmp != self.clipboard:
                        self.clipboard = tmp
                        self.node.send_all(self.clipboard)
                        self.node.data = self.clipboard
                        self.log[time.strftime(
                            "%Y-%m-%d %H:%M:%S")] = self.clipboard

                    elif tmp != self.node.data and self.node.data:
                        self.clipboard = self.node.data
                        copy(self.clipboard)

            except KeyboardInterrupt:
                self.stop()

    def stop(self):
        self.active = False
        self.node.stop()


def main():
    """
    Create a node with option to connect a remote.
    """
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--host", type=str, default=None, help="Host ip address:port (default is None which leads to random port allocation)")
    parser.add_argument("--remote", type=str, default=None, help="Remote ip address:port (default is None)")
    args = parser.parse_args()

    Session(args.host, args.remote)
