# Planes , UFOs, and  Earthquakes - Visualizing Armageddon Part 1
## Due: Wednesday October 16<sup>th</sup>

## Overview

**Data Files:**
- [earthquakes.csv](../../Resources/01_Random_Data/earthquakes.csv)
- [ufo_sightings.csv](../../Resources/01_Random_Data/ufo_sightings.csv)
- [airports.csv](../../Resources/01_Random_Data/airports.csv)

**Loading:**
- Load these into your MongoDB instance using the same techniques we used in [L04](../../Lectures/L04). 
- Since they are all location data, and since we will be querying them together, load all of them into the same database, but into seperate collections.
- Make sure you create a spatial index on each collection by adding another point field. The python code in [L04](../../Lectures/L04) creates the spatial field on the UFO collection. And the scrapbook in [L04](../../Lectures/L04) shows you how to create the index.
- Call your database "armageddon" and each collection:
  - airports
  - earthquakes
  - ufos


## Visualizing The Data

The tutorial from [medium.com](https://medium.com/analytics-vidhya/introduction-to-interactive-geoplots-with-plotly-and-mapbox-9249889358eb) shows you how to use [Plotly](https://plot.ly/python/) and [Mapbox](https://www.mapbox.com) and visualize our location data. See an example below.

| NYC Taxi Pickup Locations     |
|:----:|
|<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/nyctaxi_pickupdata.png" width="300">|

Use the methods in this tutorial to visualize each of the 3 data sets: Earthquakes, Ufo's, and Airports on a global map. Use "orange" for earthquakes. "blue" for Ufo's and "green" for airports. Below is an example with just earthquakes. 

<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/earthquake.png" width="600">


### Deliverables

- Create a folder called A07 on your repo.
- Database and collections named correctly.
- Spatial index on each collection.
- All python code necessary to create visualization.
