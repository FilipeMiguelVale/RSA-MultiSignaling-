import json
import paho.mqtt.client as mqtt
import threading
from time import sleep
import math

current_latitude = 80.0   # latitude em graus decimais
current_longitude = 0.0   # longitude em graus decimais
VELOCITY_X=5/3.6         # velocidade horizontal em m/s
VELOCITY_Y=0/3.6         # velocidade VERTICAL em m/s
TIME = 0.5               # intervalo de tempo em segundos
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("vanetza/out/cam")
    #client.subscribe("vanetza/out/spatem")
    # client.subscribe("vanetza/out/denm")
    # ...


# É chamada automaticamente sempre que recebe uma mensagem nos tópicos subscritos em cima
def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    
    #print('Topic: ' + msg.topic)
    #print('Message' + message)

    obj = json.loads(message)

    # lat = obj["latitude"]
    # ...


def next_position(latitude, longitude,velocidade_x, velocidade_y, tempo):
    """
      Calcula a próxima posição com base em coordenadas GPS e velocidade.

      Args:
        coordenadas_gps: Tupla com latitude e longitude (em graus).
        velocidade_x: Velocidade na direção x (em metros por segundo).
        velocidade_y: Velocidade na direção y (em metros por segundo).
        tempo: Tempo em segundos.

      Returns:
        Tupla com as coordenadas da próxima posição (latitude e longitude em graus).
      """

    # Converte as coordenadas GPS para radianos

    latitude_radianos = math.radians(latitude)
    longitude_radianos = math.radians(longitude)

    # Calcula a distância percorrida em cada direção
    distancia_x = velocidade_x * tempo
    distancia_y = velocidade_y * tempo

    # Calcula a nova latitude
    nova_latitude_radianos = latitude_radianos + distancia_y / (6371 * math.cos(latitude_radianos))

    # Calcula a nova longitude
    nova_longitude_radianos = longitude_radianos + distancia_x / (6371 * math.cos(latitude_radianos))

    # Converte as coordenadas de volta para graus
    nova_latitude_graus = math.degrees(nova_latitude_radianos)
    nova_longitude_graus = math.degrees(nova_longitude_radianos)

    # Retorna a próxima posição
    return nova_latitude_graus, nova_longitude_graus


def generate():
    #f = open('in_spatem.json')
    f = open('my_in_cam.json')
    m = json.load(f)
    global current_longitude
    global current_latitude
    next_latitude, next_longitude = next_position(current_latitude, current_longitude, VELOCITY_X,
                                                                   VELOCITY_Y, TIME)
    current_latitude = next_latitude
    current_longitude = next_longitude
    m["latitude"] = current_latitude
    m["longitude"] = current_longitude
    m = json.dumps(m)
    print(m)
#    client.publish("vanetza/in/spatem",m)
    client.publish("vanetza/in/cam",m)
    f.close()
    sleep(TIME)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.98.20", 1883, 60)

threading.Thread(target=client.loop_forever).start()

while(True):
    generate()
