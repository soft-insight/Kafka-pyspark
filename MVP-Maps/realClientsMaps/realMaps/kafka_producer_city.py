#!/bin/env python3

import time
import json
from kafka import KafkaProducer
import requests

kafka_bootstrap_servers = 'localhost:9092'
kafka_topic_name = 'usertopic'

producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

json_message = None
#city_name = None
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
    return json_message

#api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=af0c74adb4dfe3d002c3232d25394720
while True:
    random_api_endpoint = "https://randomuser.me/api"
    json_message = get_weather_detail(random_api_endpoint)
    type(json_message)
    producer.send(kafka_topic_name, json_message)
    print("Published message 1: " + json.dumps(json_message))
    print("Wait for 2 seconds ...")
    time.sleep(2)

"""
    city_name = "Bogota,co"
    openweathermap_api_endpoint = "http://api.openweathermap.org/data/2.5/weather?q={}&APPID=af0c74adb4dfe3d002c3232d25394720".format(city_name)
    json_message = get_weather_detail(openweathermap_api_endpoint)
    producer.send(kafka_topic_name, json_message)
    print(type(json_message))
    print("Published message 1: " + json.dumps(json_message))
    print("Wait for 2 seconds ...")
    time.sleep(2)

    city_name = "Medellin,co"
    appid  = "af0c74adb4dfe3d002c3232d25394720"
    openweathermap_api_endpoint = "http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}".format(city_name, appid)
    json_message = get_weather_detail(openweathermap_api_endpoint)
    producer.send(kafka_topic_name, json_message)
    print(type(json_message))
    print("Published message 1: " + json.dumps(json_message))
    print("Wait for 2 seconds ...")
    time.sleep(2)

    city_name = "Cali,co"
    api_site = "api.openweathermap.org/data/2.5/weather"
    appid  = "af0c74adb4dfe3d002c3232d25394720"
    openweathermap_api_endpoint = "http://{}?q={}&APPID={}".format(api_site,city_name, appid)
    json_message = get_weather_detail(openweathermap_api_endpoint)
    producer.send(kafka_topic_name, json_message)
    print(type(json_message))
    print("Published message 1: " + json.dumps(json_message))
    print("Wait for 2 seconds ...")
    time.sleep(2)
"""