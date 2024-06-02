import json
import paho.mqtt.client as mqtt
import threading
from time import sleep
import os


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

        sleep(10)


def generate():
    try:
        with open('my_in_spatem.json', 'r') as f:
            m = json.load(f)
        
        message = json.dumps(m)
        client.publish("vanetza/in/spatem", message)
        print("Generated message: ", message)
        sleep(1)
    except Exception as e:
        print("Error generating message: ", e)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(os.getenv("RSU_MQTT_IP"), int(os.getenv("RSU_MQTT_PORT")), 60)

print("Connecting to MQTT broker...")

# Start MQTT loop in a separate thread

threading.Thread(target=client.loop_forever).start()

# Start alter_state function in a separate thread
threading.Thread(target=client.loop_forever).start()

# Continuously generate and publish messages
while True:
    #generate()
    alter_state()

