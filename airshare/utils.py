import argparse


def get_args(argv=None):
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("--ip", type=str, default=None, help="")
    parser.add_argument("--port", type=int, default=None, help="")
    parser.add_argument("-c", "--clipboard", default=False, action="store_true", help="")   

    return parser.parse_args(argv)