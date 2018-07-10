import aws_mcstatus
import time
from threading import Timer

debug = True

defaultTimeout = 1 #minutes

# Initialize instance statuses
awsinstances = aws_mcstatus.initInstances(defaultTimeout)
repeatCheck = aws_mcstatus.RepeatedTimer(5, aws_mcstatus.updateStatuses, awsinstances) # it auto-starts, no need of rt.start()

while True:
    # Start main loop to check how long in state
    for i in awsinstances:
        if i.timeoutReached and i.state == 1:
            print("Shutdown {}".format(i.id))
            i.stop()
        elif i.state == 0:
            print("ID {} not running".format(i.id))
        else:
            print("ID {} not times out yet".format(i.id))
    time.sleep(60)
