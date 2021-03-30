def get_args(argv=None):
    parser = argparse.ArgumentParser(description="")
    
    parser.add_argument("-l", "--local", type=addr, default=None, help="")
    parser.add_argument("-r", "--remote", type=addr, default=None, help="")
    parser.add_argument("-c", "--clipboard", default=False, action="store_true", help="")   

    return parser.parse_args(argv)

def addr(string):
    """Format a string into an address.

    This address type takes a string in the form of host:port. It will return a
    tuple properly formatting the host as a string and the port as an int.
    """

    host, port = string.split(":")
    address = (str(host), int(port))

    return address

