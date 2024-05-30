import json
import geopy.distance
import math

simple_positions = [[(40.64196130815548, -8.651599817893402), (40.64260232822538, -8.648281407423386)],
                    [(40.6425641904421, -8.648104086128557), (40.641601012057706, -8.647785673242867)],
                    [(40.64158087763361, -8.647778626816859), (40.642531400552464, -8.648082975328139)],
                    [(40.642716577699275, -8.64798879195188), (40.6429279060416, -8.646700223922215)],
                    [(40.642882822718036, -8.6465925337987),(40.64244607644473, -8.646451422602368)],
                    [(40.64244607644473, -8.646451422602368),(40.642882822718036, -8.6465925337987)],
                    [(40.642953566928895, -8.646489987939923),(40.64397914538013, -8.641272445716009)],
                    [(40.644105963126066, -8.6414250479259),(40.643107956090425, -8.646453654080425)],
                    [(40.64314103943572, -8.646678924009313),(40.64394606245026, -8.6469550613415)],
                    [(40.64394606245026, -8.6469550613415),(40.64314103943572, -8.646678924009313)],
                    [(40.643014219856376, -8.646715257868811),(40.642777121735605, -8.647972409407442)],
                    [(40.642854316565064, -8.64820494610823),(40.64360971839902, -8.648502883756114)],
                    [(40.64360971839902, -8.648502883756114),(40.642854316565064, -8.64820494610823)],
                    [(40.64274403820994, -8.648321214458623),(40.642060308335076, -8.65155492832519)],
                    ]

current_pos = (0,0)
final_pos = (0,0)
speed = 60 / 3.6  # km /3.6 = m/s
TIME = 0.5  # seconds
current_bearing = 0
index = 1
first = True
distance = 0.005
position_index = 0;
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
    global current_bearing, index, TIME, simple_positions, final_pos, distance
    bearing = calculate_initial_compass_bearing(current_p, final_p)
    end_point = geopy.distance.distance(kilometers=distance).destination(current_pos, bearing)
    current_bearing = bearing
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


print("\n\n")
roads = []
for p in range(len(simple_positions)):
    a = [simple_positions[p][0]]

    N_Samples = int(geopy.distance.geodesic(simple_positions[p][0], simple_positions[p][1]).km / distance)
    current_pos = simple_positions[p][0]
    final_pos = simple_positions[p][1]
    for i in range(N_Samples):
      next_latitude, next_longitude = next_position(current_pos, final_pos, TIME)
      current_pos = (next_latitude, next_longitude)
      a.append(current_pos)
    a.append(simple_positions[p][1])
    roads.append(a)
    # print("list_"+str(p)+" = "+str(a))
print("roads = "+str(roads))
print("\n\n")