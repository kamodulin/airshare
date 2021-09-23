import argparse

from clipboard import Clipboard
from networking import Node


class Session:
    def __init__(self, args):

        self.host = args.host.split(":") if args.host else None
        self.remote = args.remote.split(":") if args.remote else None

        self.node = self.init_node()
        self.log = {}

        if self.remote:
            self.node.connect_to_node(str(self.remote[0]), int(self.remote[1]))

        self.clipboard = Clipboard(self.node)

    def init_node(self):
        if self.host:
            return Node(str(self.host[0]), int(self.host[1]))
        return Node()

    def prompt(self, message):
        return input(message + " ")


if __name__ == "__main__":
    """
    Create a node with option to connect a remote.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("--host", type=str, default=None, help="")
    parser.add_argument("--remote", type=str, default=None, help="")
    
    args = parser.parse_args()

    session = Session(args)