import json
import paho.mqtt.client as mqtt
import threading
from time import sleep
import os


def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code "+str(rc))
    client.subscribe("vanetza/out/spatem")
    # client.subscribe("vanetza/out/denm")
    # ...


# É chamada automatispatemente sempre que recebe uma mensagem nos tópicos subscritos em cima
def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    
    print('Topic: ' + msg.topic)
    print('Message' + message)

    obj = json.loads(message)

    # lat = obj["latitude"]
    # ...


def generate():
    f = open('my_in_spatem.json')
    m = json.load(f)
    #m["intersections"]["states"]
    m = json.dumps(m)
    client.publish("vanetza/in/spatem",m)
    f.close()
    sleep(1)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(os.getenv("RSU_MQTT_IP"), int(os.getenv("RSU_MQTT_PORT")), 60)

print("Connecting to")
threading.Thread(target=client.loop_forever).start()

while(True):
    generate()
