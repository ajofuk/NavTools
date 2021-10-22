import re
import math
from turfpy.measurement import rhumb_destination, rhumb_bearing
from geojson import Point, Feature

def get_route_data(rtefile):
    with open(rtefile, 'rt') as routefile:
        wps = re.split("waypoints =", routefile.read())

    wps = re.split("turns =", wps[1])

    trns = re.split("pim =", wps[1])
    trns = re.split("{ ", trns[0])
    wps = re.split("{ ", wps[0])
    numwps = len(wps)

    i = 1
    thisset = {}
    thisset2 = {}
    waypoints = {}
    turns = {}
    while i < numwps:
        thisset[i] = re.split('  ', wps[i])
        thisset2[i] = re.split('  ', trns[i])
        waypoints[i] = {
            "lat": float(thisset[i][1]),
            "long": float(thisset[i][2]),
            }
        turns[i] = {
            "deg": float(thisset2[i][4]),
            "adv": float(thisset2[i][2]),
            "trans": float(thisset2[i][3]),
        }
        i = i + 1
    routedata = {
        "wps": waypoints,
        "turns": turns,
    }
    return routedata

def dist_new_course(turn):
    dtnc = turn['adv'] - turn['trans'] * math.tan(90-turn['deg'])
    return dtnc

def dtr_points(waypoint, course, dtnc):
    start = Feature(geometry=Point([waypoint['long'], waypoint['lat']]))
    distance = dtnc / 2000
    course = course + 180
    while course > 180:
        course = course - 360
    bearing = course
    dtrpoints = {}
    i = 0
    while i <= 10:
        dtrpoints[i] = rhumb_destination(start, distance, bearing, {'units': 'naut'})
        distance = distance + 0.1
        i = i + 1

    return dtrpoints

def cd_bearings(dtrpoints, refpoint):
    bearing = []
    i = 0
    while i < 11:
        start = dtrpoints[i]
        end = Feature(geometry=Point([refpoint['long'], refpoint['lat']]))
        bearing.append(rhumb_bearing(start, end))
        i = i + 1
    return bearing

def leg_course(wpt_start, wpt_end):
    start = Feature(geometry=Point([wpt_start['long'], wpt_start['lat']]))
    end = Feature(geometry=Point([wpt_end['long'], wpt_end['lat']]))
    bearing = rhumb_bearing(start, end)
    return bearing



