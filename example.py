from daemonizer import Daemonizer
from multiprocessing import Event


class MySuperApp():
    def __init__(self):
        self.flag = Event()

    # Argument is optional. Pidfile only get created if you provide it though
    @Daemonizer('pidfile.pid')
    def run(self):
        import time
        while 1:
            if self.flag.is_set():
                break
            time.sleep(1)
            print("Just do it tomorrow")

    def hard_exit(self):
        print("Exiting hard way!")
        self.flag.set()

    def soft_exit(self):
        print("Exiting not so hard way!")
        import time
        time.sleep(3)
        print("Ok! It's time to exit!")
        self.flag.set()


if __name__ == '__main__':
    MySuperApp().run()
