#!/bin/env python3

from pykafka import KafkaClient
import json
from datetime import datetime
import uuid
import time
import requests
#READ COORDINATES FROM GEOJSON

client = KafkaClient(hosts="localhost:9092")
topic = client.topics['usertopic']
producer = topic.get_sync_producer() 


json_message = None
longitude = None
latitude = None
random_api_endpoint = None
appid = None

def get_weather_detail(random_api_endpoint):
    api_response = requests.get(random_api_endpoint)
    json_data = api_response.json()
    print(json_data)
    #city_name = json_data["name"]
    longitude = json_data["results"][0]["location"]["coordinates"]['longitude']
    latitude = json_data["results"][0]["location"]["coordinates"]['latitude']
    
    json_message = {
    #    "City Name": city_name,
        "longitude": longitude,
        "latitude": latitude,
        "Creation Time": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    print(type(json_message))
    return json_message

#api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=af0c74adb4dfe3d002c3232d25394720
while True:
    random_api_endpoint = "https://randomuser.me/api"
    json_message = get_weather_detail(random_api_endpoint)
    mensaje = json.dumps(json_message)
    producer.produce(mensaje.encode())
    print(mensaje)
    time.sleep(2)
#generate_checkpoint(coordinates)


