import json
import paho.mqtt.client as mqtt
import threading
from time import sleep
import geopy.distance
import math

simple_positions = [[(40.64196130815548, -8.651599817893402),(40.64260232822538, -8.648281407423386)],
[(40.6425896880125, -8.648120496512975),(40.64158087763361, -8.647778626816859)],
[(40.64158087763361, -8.647778626816859),(40.64397779517385, -8.64862076000463),],]


current_pos = (40.64196130815548, -8.651599817893402)
final_pos = (40.64260232822538, -8.648281407423386)
speed = 60/3.6  #km /3.6 = m/s
TIME = 0.5 #seconds
current_bearing = 0
index = 0
first = True
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


def next_position(current_p, final_p, tempo):
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
    global current_bearing, index, TIME, simple_positions, first, final_pos
    distance = speed * TIME / 1000
    bearing = calculate_initial_compass_bearing(current_p, final_p)

    if math.fabs(int(current_bearing)- int(bearing))>5 and not first:
        index+=1
        if index == len(simple_positions):
            index = -1
        print("index = " + str(index))
        bearing = calculate_initial_compass_bearing(current_p, simple_positions[index][1])
        final_pos = simple_positions[index][1]
        first = True
        current_bearing = bearing
        end_point = simple_positions[index][0]
    else:
        end_point = geopy.distance.distance(kilometers=distance).destination(current_pos, bearing)


    current_bearing = bearing



    if first:
        first= False
    # Retorna a próxima posição
    return end_point[0], end_point[1]

def calculate_initial_compass_bearing(pointA, pointB):
  """
  Calculates the bearing between two points.
  The formulae used is the following:
      θ = atan2(sin(Δlong).cos(lat2),
                cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
  :Parameters:
    - `pointA: The tuple representing the latitude/longitude for the
      first point. Latitude and longitude must be in decimal degrees
    - `pointB: The tuple representing the latitude/longitude for the
      second point. Latitude and longitude must be in decimal degrees
  :Returns:
    The bearing in degrees
  :Returns Type:
    float
  """
  if (type(pointA) != tuple) or (type(pointB) != tuple):
    raise TypeError("Only tuples are supported as arguments")

  lat1 = math.radians(pointA[0])
  lat2 = math.radians(pointB[0])

  diffLong = math.radians(pointB[1] - pointA[1])

  x = math.sin(diffLong) * math.cos(lat2)
  y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                         * math.cos(lat2) * math.cos(diffLong))

  initial_bearing = math.atan2(x, y)

  # Now we have the initial bearing but math.atan2 return values
  # from -180° to + 180° which is not what we want for a compass bearing
  # The solution is to normalize the initial bearing as shown below
  initial_bearing = math.degrees(initial_bearing)
  compass_bearing = (initial_bearing + 360) % 360

  return compass_bearing


def generate():
    #f = open('in_spatem.json')
    f = open('my_in_cam.json')
    m = json.load(f)
    global current_pos, final_pos
    next_latitude, next_longitude = next_position(current_pos, final_pos, TIME)
    current_pos = (next_latitude, next_longitude)
    m["latitude"] = next_latitude
    m["longitude"] = next_longitude
    m["speed"] = speed*3.6
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
