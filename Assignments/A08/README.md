## Visualizing Armageddon - Unnecessary Carnage
#### Due: 28 October by class time.

There is a new data file here: https://cs.msutexas.edu/~griffin/geo_data/plane_crashes.json

Import it like so: `mongoimport --db armageddon --collection plane_crashes --jsonArray  --file plane_crashes.json`

Perform the following using pymongo and plotly to visualize your results.

- FileName: `arm1.py`
  - Count the Ufos, Metoerites, Volcanos in every country. Print a border along with all the markers for each Ufo, Volcano, and Metoerites for the top 5 countries where top is by number of occurences. Use icons for each item unless they are so close together that they obsruct each other. If it looks good zoomed in, then that is ok. 
- FileName: `arm2.py`
  - Show the Volcanos that have the top 3 worst PEI's (Population Exposure Index). Color them red, orange, yellow respectively with larger markers for the worst. Use a volcano or mountain icon for your markers. 
- FileName: `arm3.py` 
  - Show the worst plane crashes (with Fatalities). Red over 300, Orange over 200, Yellow over 100 and blue for the rest. Use plane icons to show where they occured. 

Each file should output an html file with the same name. The html files should be placed in your cs2 server account at this path: `/home/yourusername/public_html/5303/armageddon/armX.html`

Make sure you use your own mapbox token!

