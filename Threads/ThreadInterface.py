import threading

class ThreadInterface(threading.Thread):

    def __init__(self, interface):
        super().__init__()
        self.interface = interface

    def run(self):
        while True:
            self.interface.update_interface()
