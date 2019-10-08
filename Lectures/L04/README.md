## Mongo And Python - Document Store Interface

#### Windows setup

Various links to install Python and Pip (python package manager) on windows.

- https://www.python.org/downloads/windows/
- https://docs.python.org/3/using/windows.html
- https://www.liquidweb.com/kb/install-pip-windows/
- https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation


#### UFO File

[UFO's](../../Resources/01_Random_Data/ufo_sightings.csv)

### Docker

- Install Docker
  - https://docs.docker.com/docker-for-windows/install/

- Pull a mongo Image from Docker Hub
  - `docker pull mongo`
  
- Create a local volume to persist data
  - `docker volume create --name=mongodata`

- Run your image (making it a container)
  - `docker run --name mongodb -v mongodata:/data/db -d -p 27017:27017 mongo`
    - `--name` name your container
    - `-v` mount `mongodata` (on host) : and associate it with `/data/db` (in container)
    - `-d` Run container in background and print container ID
    - `-p` Associate ports host-port:container-port
    - `mongo` the image name

- Now (per Corbin) run the following to get the shell to run:
  - `docker exec -it mongodb mongo`


- Copy the UFO file into your container:
  - `docker cp path/to/ufo_sightings.csv mongodb:/tmp/ufo_sightings.csv`

- Connect to Mongo
  - Create a db called `ufos`
  - Create a collection called `sightings`
  
- Exit Mongo

- Import all the UFO Sightings:
  - `docker exec mongodb mongoimport --db ufos --collection sightings --type csv --headerline --file /tmp/ufo_sightings.csv`
  
- Use Python to remove the bad objects (documents): 
  - `python filter_bad_docs.py` 

#### Install Cosmos DB
- Find and install Azure Cosmos DB as a VSCode Extension
- https://code.visualstudio.com/docs/azure/mongodb
- Open [THIS](./Scrapbook.Sightings.mongo) scrapbook and run.

#### Good References
- https://docs.docker.com/engine/reference/commandline/run/
- https://stackoverflow.com/questions/23735149/what-is-the-difference-between-a-docker-image-and-a-container


#### Some Basic Commands
- `docker pull imageName` - pull an image from docker hub
- `docker volume create --name=VolumeName` - create a local volume to persist data
- `docker rm 32467a32ba57` - Remove a container
- `docker stop m1` - stop container with name `m1`
- `docker ps -a ` == `docker container ls -all` list all containers
- `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name_or_id` - find ip address for container
- `docker inspect container_id` - gives a ton of info about a container
