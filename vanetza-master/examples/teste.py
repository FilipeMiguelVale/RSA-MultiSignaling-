
import geopy.distance
import math

#https://gist.github.com/jeromer/2005586
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

p1 = (40.64196130815548, -8.651599817893402)
p2 = (40.64260232822538, -8.648281407423386)
speed = 10/3.6  #km /3.6 = m/s
Time = 0.5 #seconds
distance = speed * Time/1000
bearing = calculate_initial_compass_bearing(p1,p2)


end_point = geopy.distance.distance(kilometers=distance).destination(p1, bearing)

print(end_point.latitude, end_point.longitude)