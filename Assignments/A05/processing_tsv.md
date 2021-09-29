### Processing IMDB Files

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