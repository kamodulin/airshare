import time

from pyperclip import copy, paste
from threading import Thread

class Clipboard(Thread):
    def __init__(self):
        super(Clipboard, self).__init__()
        
        self.cpb = paste()
        self.start()

    def run(self):
        while True:
            tmp = paste()

            if tmp:
                print(tmp)

            # if tmp != self.cpb:
            #     self.cpb = tmp
            #     self.node.send_all(self.cpb)
            
            # tmp = RECV
            # if tmp != self.cpb:
            #     self.cpb = tmp
            #     copy(tmp)
                
            time.sleep(1)

cpb = Clipboard()