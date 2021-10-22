import nav_functions as nf

print("Getting route data from a test route...")

routedata = nf.get_route_data('routes/50.317437R2018005.rte')

print("Displaying Latitude of Waypoint 1 and turn angle at waypoint 2. +ve indicates N'ly latitude and clockwise turn")
print(routedata['wps'][1]['lat'])
print(routedata['turns'][2]['deg'])

print("Defining a course of 300 degrees and a dtnc of 300 yds along with the lat/long of wp2, and identifying "
      "the lat/long of each distance to run point")
course = 000
dtnc = 300
dtrpoints = nf.dtr_points(routedata['wps'][2], course, dtnc)
print("All points in JSON")
print(dtrpoints)
print("Latitude at 1c to run")
print(dtrpoints[1]['geometry']['coordinates'][1])

print("Defining a reference point and calculating the bearing to it from each distance to run point")
refpoint = {
    "lat": 50.317437,
    "long": -4.159046,
    }
bearings = nf.cd_bearings(dtrpoints, refpoint)
print(bearings)
