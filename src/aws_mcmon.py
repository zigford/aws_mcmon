import aws_mcstatus
import time
from threading import Timer

class mcInstance():
    def __init__(self, id, status, stime):
        self.stime  = time.time()
        self.status = status
        self.id     = id

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def update_mc_status(instance):
    print("Hello {0}!".format(name))

awsinstances = []
i=0
for instance in aws_mcstatus.getinstances():
   #awsinstances[i] = mcInstance()
   print(instance[1])

#rt = RepeatedTimer(1, hello, "World") # it auto-starts, no need of rt.start()
try:
    time.sleep(5) # your long-running job goes here...
finally:
    rt.stop() # better in a try/finally block to make sure the program ends!
