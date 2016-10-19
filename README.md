# Daemonizer

Daemonizer is simple library (it literally contains one class) to help in daemonization of your apps. I needed it myself to daemonize one of apps I was writing at work and i loved it so much I can't get over it.  
I hope you'll like it to!

## How does it work?

`Daemonizer` class works as simple decorator which starts your app in different process and wait in original process for signals to handle exiting of your app gracefully.

It uses 2 signals `SIGINT` to soft exit and `SIGTERM` for hard exit to invoke different functions `soft_exit` and `hard_exit` respectfully from your `app` object. If you don't have those your app will just get killed by `Process.terminate` whick kinda kills the point, so I don't recomend it. 

It also allow you to create `wait` function which will run im original process and wait for signals, you can use it to get progress reports from your app or some kind of heartbeat. If you don't have those it's not a problem Daemonizer will just wait using `Process.join()`. 


## Examples? 

Yeah sure!

```
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

```



