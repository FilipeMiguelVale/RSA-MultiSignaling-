import json

from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates

import paho.mqtt.client as mqtt
import threading

OBU_MESSAGE = None
rsu_MESSAGE = None
POSTS_status = {}

ORDERING_INTENSITIES = {}

OBUS = {}
RSUS = {}

description = """
Notification API helps you do awesome stuff. 🚀

## Items


"""

app = FastAPI(title="Notification API",
    description=description,
    summary="Deadpool's favorite app. Nuff said.",
    version="1.0.1")

obu_mqtt_brokers = [
    {"broker": "192.168.98.10", "port": 1883, "topic": "vanetza/in/cam"},
    {"broker": "192.168.98.20", "port": 1883, "topic": "vanetza/in/cam"},
    {"broker": "192.168.98.30", "port": 1883, "topic": "vanetza/in/cam"},
    {"broker": "192.168.98.40", "port": 1883, "topic": "vanetza/in/cam"},

    # ...
]

rsu_mqtt_brokers = [
    {"broker": "192.168.98.100", "port": 1883, "topic": "vanetza/in/spatem"},
    {"broker": "192.168.98.110", "port": 1883, "topic": "vanetza/in/spatem"},

]



def on_connectObu1(client, userdata, flags, rc, properties):
    print("Connected to cams with result code "+str(rc))
    client.subscribe("vanetza/out/cam")

def on_connectRSU(client, userdata, flags, rc, properties):
    print("Connected to rsu with result code "+str(rc))
    client.subscribe("vanetza/out/spatem")


def on_messageRSU(client, userdata, msg):
    global rsu_MESSAGE, RSUS
    # print(colored("CAM message", "green"))
    message = json.loads(msg.payload)
    rsu_MESSAGE = msg.payload

    stationID = message["stationID"]
    #if(stationID not in RSUS):
    r = {}
    for i, group in enumerate(message["fields"]["spat"]["intersections"][0]["states"]):
        r[i]={"state": group["state-time-speed"][0]["eventState"]}
    RSUS[stationID] = r#message["fields"]["spat"]["intersections"][0]["states"][0]
    return
    #else:
    #    pass

def on_messageObu1(client, userdata, msg):
    global OBU_MESSAGE, OBUS

    message = json.loads(msg.payload)
    OBU_MESSAGE = msg.payload
    print(OBU_MESSAGE)
    longitude = message["longitude"]
    latitude = message["latitude"]
    speed = message["speed"]
    obu_id = message["stationID"]

    OBUS[obu_id] = {"longitude": longitude, "latitude": latitude, "speed": speed}



@app.get("/data", status_code=200)
async def get_mqtt_data():

    global OBUS
    return OBUS

@app.get("/dataRSU", status_code=200)
async def get_mqtt_dataRSU():

    global RSUS
    r = {}
    ii = 0
    for rsu in RSUS:
        for ind in RSUS[rsu]:
            r.update({(ind+(ii*4)) : RSUS[rsu][ind]})
        ii+=1
    return r

for broker in obu_mqtt_brokers:

    clientOBUS = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    clientOBUS.on_connect = on_connectObu1
    clientOBUS.on_message = on_messageObu1
    clientOBUS.connect(broker["broker"],broker["port"], 60)

    threading.Thread(target=clientOBUS.loop_forever).start()

for broker in obu_mqtt_brokers:

    clientRSU = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    clientRSU.on_connect = on_connectRSU
    clientRSU.on_message = on_messageRSU
    clientRSU.connect(broker["broker"],broker["port"], 60)

    threading.Thread(target=clientRSU.loop_forever).start()


