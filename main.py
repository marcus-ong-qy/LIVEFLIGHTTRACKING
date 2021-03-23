#% matplotlib tk
import urllib.request
import json
import matplotlib.pyplot as plt
from matplotlib import animation
import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM

# SET AXES
fig, ax = plt.subplots()
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_ylim(40.6051, 40.6825)
ax.set_xlim(-73.8288, -73.7258)

# ADD OSM BASEMAP
osm_tiles = OSM()
ax.add_image(osm_tiles, 13)  # Zoom Level 13

# PLOT JFK INTL AIRPORT
ax.text(-73.778889, 40.639722, 'JFK Intl', horizontalalignment='right', size='large')
ax.plot([-73.778889], [40.639722], 'bo')

# PLOT TRACK
track, = ax.plot([], [], 'ro')

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]


# UPDATE FUNCTION
def update(self):
    # SEND QUERY
    fp = opener.open(
        'http://public-api.adsbexchange.com/VirtualRadar/AircraftList.json?lat=40.639722&lng=-73.778889&fDstL=0&fDstU=20')
    mybyte = fp.read()
    mystr = mybyte.decode("utf8")
    js_str = json.loads(mystr)
    fp.close()
    lat_list = []
    long_list = []
    op_list = []  # OPERATOR LIST

    for num, flight_data in enumerate(js_str['acList']):
        lat = flight_data['Lat']
        lon = flight_data['Long']
        lat_list.append(lat)
        long_list.append(lon)
        op_list.append(flight_data['Op'])  # STORE OPERATOR DATA INTO LIST

    track.set_data(long_list, lat_list)

    # LABELING

    # REMOVE LABEL
    for num, annot in enumerate(anotation_list):
        annot.remove()
    anotation_list[:] = []

    # CREATE LABEL CONTAINER
    for num, annot in enumerate(js_str['acList']):
        annotation = ax.annotate('text', xy=(0, 0), size='smaller')
        anotation_list.append(annotation)

    # UPDATE LABEL POSITION AND OPERATOR
    for num, ano in enumerate(anotation_list):
        ano.set_position((long_list[num], lat_list[num]))
        ano.xy = (long_list[num], lat_list[num])
        txt_op = str(op_list[num])
        ano.set_text(txt_op)

    return track, ano,


# UPDATING EVERY SECOND
anim = animation.FuncAnimation(fig, update, interval=1000, blit=False)

plt.show()