import nav_functions as nf
import glob
from beautifultable import BeautifulTable

print("Notebook Calculator Tool")

route_dir = glob.glob('routes/*.rte')

print("Please select a route")
i = 1
x = len(route_dir)
while i <= len(route_dir):
    j = i-1
    print(str(i) + ") " + route_dir[j])
    i = i + 1

route_select = route_dir[int(input("Choose between 1 and " + str(len(route_dir)) + ": ")) - 1]

print("You selected " + route_select)

route_data = nf.get_route_data(route_select)

print("There are " + str(len(route_data['wps'])-1) + " legs in this route")
print("Which leg would you like to calculate data for?")
leg_select = int(input("Choose from 1 to " + str(len(route_data['wps'])-1) + ": "))
leg_course = nf.leg_course(route_data['wps'][leg_select], route_data['wps'][leg_select+1])
print("Leg " + str(leg_select) + " selected. Course: " + str(leg_course))
print("Please enter lat and long of W/O reference point")
refpoint = {}
refpoint['lat'] = float(input("Latitude: "))
refpoint['long'] = float(input("Longitude: "))
dtnc = nf.dist_new_course(route_data['turns'][leg_select+1])
dtrpoints = nf.dtr_points(route_data['wps'][leg_select], leg_course, dtnc)
cdbearings = nf.cd_bearings(dtrpoints, refpoint)

table = BeautifulTable()
table.rows.header = ['W/O', '1c', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', '1nm']
table.columns.append(cdbearings, header='Bearing')

print(table)
