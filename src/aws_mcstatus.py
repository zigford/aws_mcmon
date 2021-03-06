import boto3
import mcstatus
import argparse
import time
from threading import Timer

debug = True
client = boto3.client('ec2')

def countMcPlayers(host,port):
    server = mcstatus.MinecraftServer.lookup(host + ":" + port)
    status = server.status()
    return status.players.online
    
def getReservations():
    reservations = client.describe_instances()
    return reservations

def getInstance(id):
    r = getReservations()
    instance = None
    for res in r['Reservations']:
        for i in res['Instances']:
            if i['InstanceId'] == id:
                instance = i
    return instance

def getState(id):
    i = getInstance(id)
    if i != None:
        if i['State']['Name'] == "running":
            state = 1
        else:
            state = 0
        return state

def getHost(id):
    i = getInstance(id)
    for nic in i['NetworkInterfaces']:
        if 'Association' in nic:
            hostname = nic['Association']['PublicDnsName']
        else:
            hostname = None
    return hostname


def stopInstance(id):
    #Confirm running
    if getState(id) == 1:
        #Running. Issue shutdown
        result = client.stop_instances(InstanceIds=[id])
        print(result)
    else:
        print("{0} was not running".format(id))

def startInstance(id):
    #Confirm not running
    if getState(id) == 0:
        #Not running. Startup
        result = client.start_instances(InstanceIds=[id])
        print(result)
    else:
        print("{0} was not running".format(id))

def getinstances(timeout):
    reservations = getReservations()
    instances = []
    for reservation in reservations['Reservations']:
        for instance in reservation['Instances']:
            if instance['State']['Name'] == "running":
                state = 1
            else:
                state = 0

            for nic in instance['NetworkInterfaces']:
                if 'Association' in nic:
                    hostname = nic['Association']['PublicDnsName']
                else:
                    hostname = None
            if state == "running" and hostname:
                users = countMcPlayers(hostname,"25565")
            else:
                users = 0

            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    insName = tag['Value']

            if not insName: insName = None

            instances.append(mcInstance([instance['InstanceId'],state,hostname,users,insName],timeout))
    return instances

class mcInstance():
    def __init__(self, instance, timeout=5):
        self.stime          = time.time()
        self.id             = instance[0]
        self.state          = instance[1]
        self.host           = instance[2]
        self.users          = instance[3]
        self.name           = instance[4]
        self.timeout        = timeout
        self.timeoutReached = False

    def checkStateChange(self):
        newstate = getState(self.id)
        if self.state != newstate:
            if debug:
                print("Updating state to {}".format(newstate))
            self.state = newstate
            self.host = getHost(self.id)
            self.stime = time.time()

    def checkUserChange(self):
        if self.state == 1:
            users = countMcPlayers(self.host,"25565")
            if self.users != users:
                if debug:
                    print("Updating users to {}".format(users))
                self.users = users
                self.stime = time.time()

    def updateStatus(self):
        print("Updating status for {0}".format(self.id))
        self.checkStateChange()
        self.checkUserChange()
        if self.state == 1 and self.users == 0:
            timeout = self.stime + (self.timeout * 60)
            if time.time() > timeout:
                self.stop()
                self.timeoutReached = True

    def stop(self):
        stopInstance(self.id)

def updateStatuses(mcInstances):
    for i in mcInstances:
        i.updateStatus()

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
