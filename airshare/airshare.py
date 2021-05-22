from networking import Node
from utils import get_args


class Session:
    def __init__(self, args):
        self.remote = (str(args.ip), int(args.port)) if args.ip and args.port else None
    
        self.node = self.init_node()

        self.log = {}

        if self.remote:
            self.node.connect_to_node(*self.remote)

    def init_node(self):
        return Node()

    def prompt(self, message):
        return input(message + " ")


if __name__ == "__main__":
    """Begin a session for continuous streaming of clipboard data.

    Option to specify a local address and directly connect to remote. These are in
    the form of host:port for simplicity (e.g 192.168.0.10:8000).
    """

    args = get_args()
    session = Session(args)