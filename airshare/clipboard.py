import time

from pyperclip import copy, paste
from threading import Thread


class Clipboard(Thread):
    def __init__(self, node):
        super(Clipboard, self).__init__()

        self.node = node
        self.cpb = paste()
        self.start()

    def run(self):
        while True:
            if self.node.connections:
                tmp = paste()
                
                print(tmp)

                if tmp != self.cpb:
                    self.cpb = tmp
                    self.node.send_all(self.cpb)
                    self.node.data = self.cpb

                elif tmp != self.node.data and self.node.data:
                    self.cpb = self.node.data
                    copy(self.cpb)

                time.sleep(1)
                
            else:
                time.sleep(5)