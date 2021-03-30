import argparse

from networking import Node
from utils import addr, get_args


class Session:
    def __init__(self, args):
        self.local = args.local
        self.remote = args.remote

        self.node = self.init_node()

        self.log = {}

        if self.remote:
            self.node.connect_to_node(*self.remote)

    def init_node(self):
        return Node(*self.local) if self.local else Node()

    def prompt(self, message):
        return input(message + " ")


if __name__ == "__main__":
    """Begin a session for continuous streaming of clipboard data.

    Option to specify a local address and directly connect to remote. These are in
    the form of host:port for simplicity (e.g 192.168.0.10:8000).
    """

    args = get_args()
    session = Session(args)