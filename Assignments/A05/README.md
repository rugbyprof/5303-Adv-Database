## Assignment 5 - Movies DB.
#### Due: 09-27-2021 (Monday @ 5:00 p.m.)


### References For You  

* https://realpython.com/python-mysql/
* https://realpython.com/fastapi-python-web-apis/
* https://realpython.com/api-integration-in-python/
* https://datasets.imdbws.com/

#### Unicode!!
* https://realpython.com/python-encodings-guide/

### Overview

We have a huge amount of data given to us by the IMDB website in 7 different files. The overall goal is to create your own local database of the movie data using the files located at the following address:
https://datasets.imdbws.com/. This will of course involve a many stage process.

* Getting all files
* Uncompressing the files.
* Processing each file into a usable format OR 
* Re-Organize the files by filtering / combining them to fit a schema



### File Data Overview

Each dataset is contained in a gzipped, tab-separated-values (TSV) formatted file in the UTF-8 character set. The first line in each file contains headers that describe what is in each column. A `\N` is used to denote that a particular field is missing or null for that title/name. The available datasets are as follows:

* **title.akas.tsv.gz** - Contains the following information for titles:

  * titleId (string) - a tconst, an alphanumeric unique identifier of the title
  * ordering (integer) – a number to uniquely identify rows for a given titleId
  * title (string) – the localized title
  * region (string) - the region for this version of the title
  * language (string) - the language of the title
  * types (array) - Enumerated set of attributes for this alternative title. One or more of the following: "alternative", "dvd", "festival", "tv", "video", "working", "original", "imdbDisplay". New values may be added in the future without warning
  * attributes (array) - Additional terms to describe this alternative title, not enumerated
  * isOriginalTitle (boolean) – 0: not original title; 1: original title

* **title.basics.tsv.gz** - Contains the following information for titles:
  * tconst (string) - alphanumeric unique identifier of the title
  * titleType (string) – the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)
  * primaryTitle (string) – the more popular title / the title used by the filmmakers on promotional materials at the point of release
  * originalTitle (string) - original title, in the original language
  * isAdult (boolean) - 0: non-adult title; 1: adult title
  * startYear (YYYY) – represents the release year of a title. In the case of TV Series, it is the series start year
  * endYear (YYYY) – TV Series end year. ‘\N’ for all other title types
  * runtimeMinutes – primary runtime of the title, in minutes
  * genres (string array) – includes up to three genres associated with the title

* **title.crew.tsv.gz** – Contains the director and writer information for all the titles in IMDb. Fields include:
  * tconst (string) - alphanumeric unique identifier of the title
  * directors (array of nconsts) - director(s) of the given title
  * writers (array of nconsts) – writer(s) of the given title

* **title.episode.tsv.gz** – Contains the tv episode information. Fields include:
  * tconst (string) - alphanumeric identifier of episode
  * parentTconst (string) - alphanumeric identifier of the parent TV Series
  * seasonNumber (integer) – season number the episode belongs to
  * episodeNumber (integer) – episode number of the tconst in the TV series

* **title.principals.tsv.gz** – Contains the principal cast/crew for titles
  * tconst (string) - alphanumeric unique identifier of the title
  * ordering (integer) – a number to uniquely identify rows for a given titleId
  * nconst (string) - alphanumeric unique identifier of the name/person
  * category (string) - the category of job that person was in
  * job (string) - the specific job title if applicable, else '\N'
  * characters (string) - the name of the character played if applicable, else '\N'

* **title.ratings.tsv.gz** – Contains the IMDb rating and votes information for titles
  * tconst (string) - alphanumeric unique identifier of the title
  * averageRating – weighted average of all the individual user ratings
  * numVotes - number of votes the title has received

* **name.basics.tsv.gz** – Contains the following information for names:
  * nconst (string) - alphanumeric unique identifier of the name/person
  * primaryName (string)– name by which the person is most often credited
  * birthYear – in YYYY format
  * deathYear – in YYYY format if applicable, else '\N'
  * primaryProfession (array of strings)– the top-3 professions of the person
  * knownForTitles (array of tconsts) – titles the person is known for


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



### Example Schema

```sql
CREATE TABLE actor
  (
     id        INT(6),
     firstname VARCHAR(100),
     lastname  VARCHAR(100),
     gender    CHAR(1),
     PRIMARY KEY (id)
  );

CREATE TABLE director
  (
     id        INT(6),
     firstname VARCHAR(100),
     lastname  VARCHAR(100),
     PRIMARY KEY (id)
  );

CREATE TABLE genre
  (
     genre VARCHAR(20),
     PRIMARY KEY (genre)
  );

CREATE TABLE directorgenre
  (
     directorid  INT(6),
     genre       VARCHAR(20),
     probability FLOAT(12, 10),
     FOREIGN KEY (directorid) REFERENCES director(id),
     FOREIGN KEY (genre) REFERENCES genre(genre)
  );

CREATE TABLE movie
  (
     id       INT(6),
     NAME     VARCHAR(100),
     year     INT(4),
     rank     FLOAT(10, 2),
     sequelid INT(6),
     PRIMARY KEY (id),
     FOREIGN KEY (sequelid) REFERENCES movie(id)
  );

CREATE TABLE moviedirector
  (
     directorid INT(6),
     movieid    INT(6),
     FOREIGN KEY (directorid) REFERENCES director(id),
     FOREIGN KEY (movieid) REFERENCES movie(id)
  );

CREATE TABLE moviegenre
  (
     movieid INT(6),
     genre   VARCHAR(20),
     FOREIGN KEY (movieid) REFERENCES movie(id),
     FOREIGN KEY (genre) REFERENCES genre(genre)
  );

CREATE TABLE role
  (
     actorid INT(6),
     movieid INT(6),
     role    VARCHAR(100),
     FOREIGN KEY (actorid) REFERENCES actor(id),
     FOREIGN KEY (movieid) REFERENCES movie(id)
  ); 
```


<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/imdb_schema.png" width="600">


### Example Code



Downloading the files from IMDB:

```bash
wget https://datasets.imdbws.com/ -r -l1 --no-parent -A ".gz"
```

Uncompress the files:

```bash
cd datasets.imdbws.com/
gunzip *.gz
```

Processing the TSV files using the python CSV library

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

"""
Process files here....
"""
```


### Routes 

* Using https://realpython.com/fastapi-python-web-apis/ create a folder on your server `/var/www/html/Apis/movie` and implement an API for the movies DB.

- BRAINSTORMING SESSION ON POSSIBLE QUERIES.


### Deliverables

* Create a page that shows all routes so they can be clicked on to run when I go here: http://Your.IP.Address:8002/
* I should see all of your routes or if you can add to the docs some how, that would be sufficient when  going here: http://Your.IP.Address:8002/docs 

