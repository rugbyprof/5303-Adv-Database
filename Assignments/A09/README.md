## DB Testing - Comparing Performance
#### TBD

#### Python2 vs Python3

- Remember that any instructions using `pip install` usually defaults to `python2`. We want to default to python 3, so make sure you are using the correct version of python.
- First, you can check for the default version of python:
  - `python --version` 
  - If python 3 shows up, good.
- Otherwise, lets see if python3 is installed.
  - `which python3`
  - If a path shows up, good.
  - If not: `brew install python3`
- On a mac, you can see if `pip3` is installed by typing:
  - `which pip3`
  - If a path shows up, good, it not:
    - `brew install python3`
    - `brew postinstall python3`

### Neo4J

- Installing on a Mac:
  - https://code2bits.com/how-to-install-neo4j-on-macos-using-homebrew/
- Setting Up Cluster
  - https://neo4j.com/docs/operations-manual/current/clustering/setup-new-cluster/
- Python + Neo4J
  - https://neo4j.com/developer/python/

### Redis

- Installing on a Mac:
  - https://gist.github.com/tomysmile/1b8a321e7c58499ef9f9441b2faa0aa8
- Redis Cluster
  - https://cleanprogrammer.net/setting-up-a-high-available-multi-node-redis-cluster/
- Python + Redis
  - https://realpython.com/python-redis/


### CouchBase

- Install Couchbase
  - https://code2bits.com/how-to-install-couchbase-community-edition-on-macos-using-homebrew/
- Install Cluster
  - https://docs.couchbase.com/server/4.1/clustersetup/manage-cluster-intro.html
- Python + Couchbase
  - https://docs.couchbase.com/python-sdk/current/start-using-sdk.html


### CouchDB

- Install Couchbase
  - https://docs.couchdb.org/en/1.6.1/install/mac.html
- Install Cluster
  - https://docs.couchbase.com/server/current/install/install-intro.html
- Python + CouchDB
  - https://couchdb-python.readthedocs.io/en/latest/

### Mongo

- Install Mongo
  - https://treehouse.github.io/installation-guides/mac/mongo-mac.html
- Cluster
  - https://www.guru99.com/top-20-mongodb-tools.html
  - https://severalnines.com/product/clustercontrol/clustercontrol-community-edition
- Python + Mongo
  - https://realpython.com/introduction-to-mongodb-and-python/

### Apache Cassandra

- Install Cassandra
    - https://medium.com/@areeves9/cassandras-gossip-on-os-x-single-node-installation-of-apache-cassandra-on-mac-634e6729fad6
  - OR
    - https://gist.github.com/mars/a303a2616f27b46d72da
- Cluster Recources
  - https://academy.datastax.com/planet-cassandra/getting-started-with-ccm-cassandra-cluster-manager