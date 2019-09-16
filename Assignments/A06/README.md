# Barebones Refactor - Worst Flight Planner Step 3

## Due: Monday September 23<sup>rd</sup>

## Overview

Generate your best "worst" flight path and output it using [geojson](https://geojson.org/) as a visualization tool. Here are a few resources to help with geojson:

- [Specification](https://geojson.org/) Home page of geo json specification.
- [Tutorial](https://medium.com/@sumit.arora/what-is-geojson-geojson-basics-visualize-geojson-open-geojson-using-qgis-open-geojson-3432039e336d) A nice overview of the different geometries.
- [Styling](https://github.com/mapbox/simplestyle-spec/tree/master/1.1.0) How to add color, comments, and change markers.
- [Markers](https://gis.stackexchange.com/questions/219241/list-of-available-marker-symbols) Different markers that can be used.
- [Software](https://github.com/tmcw/awesome-geojson) Software that can be used to create, edit, or view geojson. Not necessary for this assignment.
- [Formatter](https://jsonformatter.curiousconcept.com/) Convenient formatter to make json (and geojson) more readable. Not necessary for assignment.
- [Viewer/Builder](http://geojson.io) Interactive geojson editor and viewer website.

By generating GeoJson as your output, you can create a very readable and clear visualization of your generated route without any additional programming. Github automatically shows the results of any file with a `.geojson` extension. [Here](https://github.com/rugbyprof/5303-Adv-Database/blob/master/Resources/04_GeoJsonExample/example.geojson) is an example.

## Route Specifications

Lets generate multiple kinds of routes. The goal is to get to some destination, but with a lot of sight seeing along the way.

1. All the countries
2. All the continents
3. In a circle (or polygon)
4. Around the world

We will discuss parameters in class, and will allow the specs to change if problems arise.

Obviously we will need the [Mysql spatial convenience functions](https://dev.mysql.com/doc/refman/5.7/en/spatial-convenience-functions.html), but we will also need to perform some other querying techniques as well.

## Database

Create a table:

column      | type
:---------- | :------------
id          | int
geojson     | json
type        | enum(1,2,3,4)
description | text
query       | text

## Deliverables

- Create a folder called A06 on your repo.
- Inside this folder, place all of your queries in a markdown doc with syntax highlighted queries and a link to the geojson file (route) it created.

