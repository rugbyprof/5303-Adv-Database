### Assignment 5 - Movies DB.
#### Due: 09-27-2021 (Monday @ 5:00 p.m.)


### References For You  

* https://realpython.com/python-mysql/
* https://realpython.com/fastapi-python-web-apis/
* https://realpython.com/api-integration-in-python/
* https://datasets.imdbws.com/

#### Unicode!!
* https://realpython.com/python-encodings-guide/

### Overview

* Create your own local database of the Movie data using the data files located at the following address:
https://datasets.imdbws.com/


* Get all files from website:
  * `wget https://datasets.imdbws.com/ -r -l1 --no-parent -A ".gz"`
* Change into the `datasets.imdbws.com` folder that got created and uncompress each file.
  * `gunzip *.gz`

* Using https://realpython.com/fastapi-python-web-apis/ create a folder on your server `/var/www/html/Apis/movie` and implement an API for the movies DB.


### File Data Overview

#### title.basics.tsv

```
    tconst	titleType	primaryTitle	originalTitle	isAdult	startYear	endYear	runtimeMinutes	genres
    tt0000001	short	Carmencita	Carmencita	0	1894	\N	1	Documentary,Short
    tt0000002	short	Le clown et ses chiens	Le clown et ses chiens	0	1892	\N	5	Animation,Short
```

#### title.episode.tsv

```
    tconst	parentTconst	seasonNumber	episodeNumber
    tt0020666	tt15180956	1	2
```

#### title.ratings.tsv

```
    tconst	averageRating	numVotes
    tt0000001	5.7	1816
```

#### name.basics.tsv

```
    nconst	primaryName	birthYear	deathYear	primaryProfession	knownForTitles
    nm0000001	Fred Astaire	1899	1987	soundtrack,actor,miscellaneous	tt0072308,tt0053137,tt0050419,tt0031983
    nm0000002	Lauren Bacall	1924	2014	actress,soundtrack	tt0038355,tt0071877,tt0117057,tt0037382
```

#### title.akas.tsv

```
    titleId	ordering	title	region	language	types	attributes	isOriginalTitle
    tt0000001	1	Карменсіта	UA	\N	imdbDisplay	\N	0
    tt0000001	2	Carmencita	DE	\N	\N	literal title	0
    tt0000001	3	Carmencita - spanyol tánc	HU	\N	imdbDisplay	\N	0
```

#### title.crew.tsv

```
    tconst	directors	writers
    tt0000001	nm0005690	\N
    tt0000007	nm0005690,nm0374658	\N
```

#### title.principals.tsv

```
    tconst	ordering	nconst	category	job	characters
    tt0000001	1	nm1588970	self	\N	["Self"]
    tt0000001	2	nm0005690	director	\N	\N
    tt0000001	3	nm0374658	cinematographer	director of photography	\N
```

```py
from mysqlCnx import MysqlCnx
import csv
import glob
import json


files = glob.glob('datasets.imdbws.com/*.tsv')


for file in files:
    print(file)
    with open(file, newline='\n') as tsvfile:
        movieData = csv.reader(tsvfile, delimiter='\t', quotechar='')
        for row in movieData:
          print(', '.join(row))


```

### Routes 


### Examples:



### Deliverables

* Create a page that shows all routes so they can be clicked on to run when I go here: http://Your.IP.Address:8002/
* I should see all of your routes or if you can add to the docs some how, that would be sufficient when  going here: http://Your.IP.Address:8002/docs 

