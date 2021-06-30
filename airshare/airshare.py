from clipboard import Clipboard
from networking import Node
from utils import get_args


class Session:
    def __init__(self, args):
        self.remote = (str(args.ip), int(args.port)) if args.ip and args.port else None
    
        self.node = self.init_node()
        self.log = {}

        if self.remote:
            self.node.connect_to_node(*self.remote)

        if args.clipboard:
            self.clipboard = Clipboard(self.node)

    def init_node(self):
        return Node()

    def prompt(self, message):
        return input(message + " ")


if __name__ == "__main__":
    """
    Create a node with options to connect a remote and share host clipboard.
    """

    args = get_args()
    session = Session(args)