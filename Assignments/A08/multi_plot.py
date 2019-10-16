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

# init the map figure
fig = go.Figure()


# I will use later
shape = get_country_geojson("Turkey")


# Get meteorite data
mlats,mlons = get_meteorites()

"""
Add a bunch of markers for Meteorites
"""
fig.add_trace(go.Scattermapbox(
                    lon=mlons, 
                    lat=mlats,
                    mode='markers',
                    name='Meteorites',
                    marker=go.scattermapbox.Marker(
                        size=3
                    )
                )
            )

# Get Ufo data
ulats,ulons = get_ufos()

"""
Add a bunch of markers for Ufos
"""
fig.add_trace(go.Scattermapbox(
                    lon=ulons, 
                    lat=ulats,
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

# Get the lat lons for Turkey's border
country = get_country_border("Turkey")

# Create  bounding boxing around Turkey
bbox = get_bbox(country)

# Convert the bounding box to a drawable box
dlats,dlons = draw_bbox(bbox)

"""
Add a bounding box around Turkey
"""
fig.add_trace(go.Scattermapbox(
    lat = dlats,
    lon = dlons,
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