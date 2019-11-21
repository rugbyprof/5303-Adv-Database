#!/usr/local/bin/python3

import plotly
import plotly.graph_objects as go

# Import all my functions from geo.py
from geo import mapbox_access_token
from geo import get_country_border
from geo import get_bbox
from geo import get_meteorites
from geo import get_ufos
from geo import draw_bbox
from geo import get_country_geojson
from geo import get_within_box
from geo import get_center_point




brazil_border = get_country_border("Brazil")

brazil_center = get_center_point(brazil_border['lonlat'])

turkey_border = get_country_border("Turkey")

# Create  bounding boxing around Turkey
turkey_bbox = get_bbox(turkey_border)

# Convert the bounding box to a drawable box
turkey_box_lats,turkey_box_lons = draw_bbox(turkey_bbox)

ufos_in_turkey = get_within_box("ufos",turkey_bbox)

turkey_ufo_lats = []
turkey_ufo_lons = []
for tufo in ufos_in_turkey:
    turkey_ufo_lats.append(tufo['latitude'])
    turkey_ufo_lons.append(tufo['longitude'])

# Get meteorite data
meteor_lats,meteor_lons = get_meteorites()

# Get Ufo data
ufo_lats,ufo_lons = get_ufos()

# init the map figure
fig = go.Figure()



"""
Add a bunch of markers for Meteorites
"""
fig.add_trace(go.Scattermapbox(
                    lon=meteor_lons, 
                    lat=meteor_lats,
                    mode='markers',
                    name='Meteorites',
                    marker=go.scattermapbox.Marker(
                        size=3
                    )
                )
            )



"""
Add a bunch of markers for Ufos
"""
fig.add_trace(go.Scattermapbox(
                    lon=ufo_lons, 
                    lat=ufo_lats,
                    mode='markers',
                    name='Ufos',
                    marker=go.scattermapbox.Marker(
                        size=3
                    )
                )
            )

"""
Draw a line from NY to London
"""
fig.add_trace(go.Scattermapbox(
    lat = [40.7127, 51.5072],
    lon = [-74.0059, 0.1275],
    mode = 'lines',
    name='NY to London',
    line = dict(width = 2, color = 'blue'),
))


"""
Add a bunch of markers for Ufos in Turkey this time
"""
fig.add_trace(go.Scattermapbox(
                    lon=turkey_ufo_lons, 
                    lat=turkey_ufo_lats,
                    mode='markers',
                    name='Turkey_Ufos',
                    marker=go.scattermapbox.Marker(
                        size=5,
                        color='green'
                    )
                )
            )


"""
Add a bounding box around Turkey
"""
fig.add_trace(go.Scattermapbox(
    lat = turkey_box_lats,
    lon = turkey_box_lons,
    mode = 'lines',
    name='Turkey',
    line = dict(width = 2, color = 'green')
))




fig.update_layout(
    hovermode='closest',
    template="plotly_dark",
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=1,
            lon=1
        ),
        pitch=0,
        zoom=3
        
    )
)

fig.show()
#plotly.offline.plot(fig, filename='multi.html')