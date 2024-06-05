import json
import paho.mqtt.client as mqtt
import threading
from time import sleep
import os

rsu_mqtt_brokers = [
    {"broker": "192.168.98.100", "port": 1883, "topic": "vanetza/in/spatem"},
    {"broker": "192.168.98.110", "port": 1883, "topic": "vanetza/in/spatem"},

]
clients = []

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))
    client.subscribe("vanetza/out/spatem")
    # client.subscribe("vanetza/out/denm")
    # ...


def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    
    print('Topic: ' + msg.topic)
    print('Message: ' + message)

    obj = json.loads(message)


def alter_state():
    while True:
        for client in clients:
            try:
                with open('my_in_spatem.json', 'r') as f:
                    m = json.load(f)

                #print("Original state: ", json.dumps(m, indent=4))

                for state in m["intersections"][0]["states"]:
                    for sts in state["state-time-speed"]:
                        print("State before change:", sts)
                        if sts["eventState"] == 3:
                            sts["eventState"] = 4
                        elif sts["eventState"] == 4:
                            sts["eventState"] = 6
                        else:
                            sts["eventState"] = 3
                        print("State after change:", sts)

                with open('my_in_spatem.json', 'w') as f:
                    json.dump(m, f, indent=4)

                message = json.dumps(m)
                client.publish("vanetza/in/spatem", message)
                print("Published updated state: ", message)
            except Exception as e:
                print("Error updating state: ", e)

        sleep(5)


def generate():
    try:
        with open('my_in_spatem.json', 'r') as f:
            m = json.load(f)
        
        message = json.dumps(m)
        clients[0].publish("vanetza/in/spatem", message)
        print("Generated message: ", message)
        sleep(1)
    except Exception as e:
        print("Error generating message: ", e)

for broker in rsu_mqtt_brokers:

    clientRSU = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    clientRSU.on_connect = on_connect
    clientRSU.on_message = on_message
    clientRSU.connect(broker["broker"],broker["port"], 60)
    clients.append(clientRSU)
    threading.Thread(target=clientRSU.loop_forever).start()



# Continuously generate and publish messages
while True:
    #generate()
    alter_state()

