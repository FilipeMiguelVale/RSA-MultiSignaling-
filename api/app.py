import json

from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Request
from routers import register
from fastapi.templating import Jinja2Templates

import paho.mqtt.client as mqtt
import threading

OBU_MESSAGE = None
rsu_MESSAGE = None
POSTS_status = {}

ORDERING_INTENSITIES = {}

OBUS = {}

description = """
Notification API helps you do awesome stuff. 🚀

## Items


"""

app = FastAPI(title="Notification API",
    description=description,
    summary="Deadpool's favorite app. Nuff said.",
    version="1.0.1",
    root_path="/api/v1")

mqtt_brokers = [
    {"broker": "192.168.98.20", "port": 1883, "topic": "vanetza/in/cam"},
    {"broker": "192.168.98.10", "port": 1883, "topic": "vanetza/in/cam"},
    # ...
]
mqtt_broker = "192.168.98.20"
mqtt_port = 1883
mqtt_topic = "vanetza/in/cam"

global last_message

def on_connectObu1(client, userdata, flags, rc):
    print("Connected to cams with result code "+str(rc))
    client.subscribe("vanetza/out/cam")

def on_messageObu1(client, userdata, msg):
    global OBU_MESSAGE, OBUS
    # print(colored("CAM message", "green"))
    message = json.loads(msg.payload)
    OBU_MESSAGE = msg.payload
    longitude = message["longitude"]
    latitude = message["latitude"]
    speed = message["speed"]
    obu_id = message["stationID"]

    if(obu_id not in OBUS):
        OBUS[obu_id] = {"longitude": longitude, "latitude": latitude, "speed": speed}
        return
    else:
        OBUS[obu_id]["longitude"] = longitude
        OBUS[obu_id]["latitude"] = latitude
        OBUS[obu_id]["speed"] = speed


@app.get("/data")
def get_mqtt_data():
    """
    Endpoint GET para ler informações de vários clusters MQTT.
    """

    global OBUS
    # print(OBUS)
    return OBUS, 200

for broker in mqtt_brokers:
#connect to obu
    clientOBUS = mqtt.Client()
    clientOBUS.on_connect = on_connectObu1
    clientOBUS.on_message = on_messageObu1
    clientOBUS.connect(broker["broker"],broker["port"], 60)

    threading.Thread(target=clientOBUS.loop_forever).start()
