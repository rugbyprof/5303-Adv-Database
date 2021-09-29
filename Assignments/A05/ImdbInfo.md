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
