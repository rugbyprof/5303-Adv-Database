import pymongo  # package for working with MongoDB

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["armageddon"]

## GET YOUR OWN!!
mapbox_access_token = "pk.eyJ1IjoicnVnYnlwcm9mIiwiYSI6ImNpZ3M1aDZwbzAyMnF1c20xcnM4ZGowYWQifQ.s6ghscOu98he230FV1_72w"


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

def get_bbox(points):
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

    return {"lon":(min_lon + max_lon)/2,"lat":(min_lat + max_lat)/2,"min_lat":min_lat,"max_lat":max_lat,"min_lon":min_lon,"max_lon":max_lon}

def within_bbox(bbox,lat,lon):
    return (lat < bbox['max_lat'] and lat > bbox['min_lat'] and lon < bbox['max_lon'] and lon > bbox['min_lon'])

def get_meteorites():
    meteors = db["meteorites"]
    lats = []
    lons = []
    for obj in meteors.find():
        latlon = obj['GeoLocation'][1:-1]
        if len(latlon.strip()) > 0:
            lat,lon = latlon.split(',')
            lat = float(lat)
            lon = float(lon)
            #if within_bbox(bbox,lat,lon):
            lats.append(lat)
            lons.append(lon)
    return (lats,lons)