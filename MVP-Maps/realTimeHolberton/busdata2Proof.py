#!/bin/env python3

from pykafka import KafkaClient
import json
from datetime import datetime
import uuid
import time

#READ COORDINATES FROM GEOJSON

input_file = open('./dataProof/bus2.json')
print(input_file)

json_array = json.load(input_file)
print(json_array['features'][0]['geometry']['coordinates'][0])
coordinates = json_array['features'][0]['geometry']['coordinates']

def generate_uuid():
    return uuid.uuid4()

"""KAFKA PRODUCER
"""

client = KafkaClient(hosts="localhost:9092")
topic = client.topics['geodatafinal']
producer = topic.get_sync_producer()



"""CONSTRUCT MESSAGE -- SENT IT TO KAFKA
"""

data = {}

data['busline'] = '00002'

def generate_checkpoint(coordinates):
    i = 0
    while i < len(coordinates):
        data['key'] = data['busline'] + str(generate_uuid())
        data['timestamp'] = str(datetime.now())
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        message = json.dumps(data)
        print(message)
        producer.produce(message.encode('utf-8'))
        time.sleep(1)

        if i == len(coordinates) - 1:
            i = 0
        else:
            i += 1


generate_checkpoint(coordinates)




"""
#KAFKA PRODUCER
client = KafkaClient(hosts="localhost:9092")



print(client.topics)
print(client.topics['testBusdata'])

topic = client.topics['testBusdata']

proofProduce = topic.get_sync_producer()

proofProduce.produce('test message'.encode('utf-8'))

count = 1
while True:
    message = ("Hello - {}".format(count)).encode('utf-8')
    proofProduce.produce(message)
    print(message)
    count += 1
"""

