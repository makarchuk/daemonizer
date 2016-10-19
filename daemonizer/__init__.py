import os
import sys
import multiprocessing
import signal


class Daemonizer():
    def __init__(self, pid_file=''):
        self.obj = None
        self.pid_file = pid_file
        self.proc = None

    def __call__(self, func):
        def runable(obj, *args, **kwargs):
            self.obj = obj
            self.proc = multiprocessing.Process(target=func,
                                                args=tuple([obj] + list(args)),
                                                kwargs=kwargs)
            with self:
                self.proc.start()
                signal.signal(signal.SIGTERM, self.sigterm_handle)
                signal.signal(signal.SIGINT, self.sigint_handle)
                if getattr(obj, "wait", None) and callable(obj.wait):
                    obj.wait()
                else:
                    self.wait_for_signals()
                return True

        return runable

    def __enter__(self):
        if self.pid_file:
            self.create_pid_file()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.pid_file:
            self.remove_pid_file()
        pass

    def create_pid_file(self):
        pid = str(os.getpid())
        with open(self.pid_file, "w") as f:
            f.write(pid)

    def remove_pid_file(self):
        os.remove(self.pid_file)

    def wait_for_signals(self):
        while 1:
            pass

    def sigterm_handle(self, signum, frame):
        self.hard_exit()

    def sigint_handle(self, signum, frame):
        self.soft_exit()

    def hard_exit(self):
        if self.obj and callable(getattr(self.obj, 'hard_exit', None)):
            self.obj.hard_exit()
            self.proc.join()
        else:
            self.proc.terminate()
        sys.exit(0)

    def soft_exit(self):
        if self.obj and callable(getattr(self.obj, 'soft_exit', None)):
            self.obj.soft_exit()
            self.proc.join()
        else:
            self.hard_exit()
        sys.exit(0)
