#!/usr/local/bin/python3

import plotly
import plotly.graph_objects as go
from geo import mapbox_access_token
from geo import get_country_border
from geo import get_center_point



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
