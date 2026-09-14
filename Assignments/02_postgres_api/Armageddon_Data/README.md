## Armageddon Data

### zip_manager.py

This manager is for Griffin because the size of the repo is growing really fast and I needed a way to shrink files by zipping them. However, if I add all the files to the same archive, that filesize is still huge. So I run `python zip_manager.py zip` to zip every file, add a .(dot) in front of the geojson, json, and csv files so they won't get pushed to github.

For you students, just run: `python zip_manager.py unzip` to unzip each file to get your geojson, json, and csv files back.

### Usage:

```sh
python zip_manager.py zip [directory]
```

- Compress all .json, .geojson, and .csv files into individual .zip archives, then rename the originals to hidden dot-files (e.g. data.csv -> .data.csv) so they are excluded from git commits.
- Skips files already up to date.

```sh
python zip_manager.py unzip [directory]
```

- Extract all .zip files into the same directory, restoring original filenames.
- Skips files whose extracted content already matches the zip.

- **_[directory]_** is optional and defaults to the current working directory.

### Examples:

```sh
python zip_manager.py zip
python zip_manager.py zip /path/to/data
python zip_manager.py unzip
python zip_manager.py unzip /path/to/data
```

#### Workflow:

1. Run `zip` to compress data files and hide the originals with a dot-prefix.
2. Commit only the .zip files.
3. My .gitignore excludes all .(dot) files:

```
.*
!.gitignore
```

4. Collaborators run `unzip` after cloning/pulling to restore working files.
5. To update a file: rename .filename.ext back to filename.ext edit it,then run `zip` again.
