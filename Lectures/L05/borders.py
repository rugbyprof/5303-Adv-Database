#!/usr/local/bin/python3

import plotly
import plotly.graph_objects as go
import pymongo  # package for working with MongoDB

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["armageddon"]


mapbox_access_token = "GET YOUR OWN TOKEN FROM MAPBOX"

def get_country_border(country):
    global db
    countries = db["countries"]

    lines = []
    points = {'lat':[],'lon':[],'latlon':[]}

    for obj in countries.find({"properties.ADMIN" : country}, { "geometry.coordinates": 1, "_id": 0 }):
        lines.append(obj)
    
    for group in lines[0]['geometry']['coordinates']:
        #print(group)
        for line in group:
            #print(line)
            for point in line:
                points['lat'].append(point[1])
                points['lon'].append(point[0])
                points['latlon'].append(point)

    return points

def get_center_point(points):
    min_lat = 90
    max_lat = -90
    min_lon = 180
    max_lon = -180

    for point in points:
        if point[1] < min_lat:
            min_lat = point[1]
        if point[0] < min_lon:
            min_lon = point[0]
        if point[1] > max_lat:
            max_lat = point[1]
        if point[0] > max_lon:
            max_lon = point[0]

    return {"lon":(min_lon + max_lon)/2,"lat":(min_lat + max_lat)/2}

points = get_country_border("Brazil")

center = get_center_point(points['latlon'])

fig = go.Figure(go.Scattermapbox(
        lat=points['lat'],
        lon=points['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=1
        ),
        #text=['Montreal'],
        
    ))

fig.update_layout(
    hovermode='closest',
    template="plotly_dark",
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=center['lat'],
            lon=center['lon']
        ),
        pitch=0,
        zoom=3
        
    )
)

fig.show()
plotly.offline.plot(fig, filename='border.html')
