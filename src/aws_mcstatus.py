import boto3
import mcstatus
import argparse

def countMcPlayers(host,port):
    server = mcstatus.MinecraftServer.lookup(host + ":" + port)
    status = server.status()
    return status.players.online
    
client = boto3.client('ec2')
reservations = client.describe_instances()

def getinstances():
    for reservation in reservations['Reservations']:
        for instance in reservation['Instances']:
            state = instance['State']['Name']
            for nic in instance['NetworkInterfaces']:
                if 'Association' in nic:
                    hostname = nic['Association']['PublicDnsName']
                else:
                    hostname = None

            return [instance['InstanceId'],state,hostname]
