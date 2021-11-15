## Assignment 9 - Presentations
#### Due: 12-06-2021 (Monday @ 5:45 p.m.)

## Individual Assignments
- A03
  - A digital ocean server with your github repository cloned on it.
  - Mysql and PhpMyadmin working
  - I should be able to log in per instructions.


### A04: Sqlzoo Debacle
  - Your SQLZoo assignment with associated tables should exist.
  - Api running on port 8001
  
#### Routes
>   * Basics
>     * Sqlzoo Problem Set: https://sqlzoo.net/wiki/SELECT_basics
>     * Route Name : basics
>     * Example Route: http://Your.IP.Address:8001/basics/   (returns all queries)
>     * Example Route: http://Your.IP.Address:8001/basics/{id}
>   * World Tutorial
>     * Sqlzoo Problem Set: https://sqlzoo.net/wiki/SELECT_from_WORLD_Tutorial
>     * Route Name : world
>     * Example Route: http://Your.IP.Address:8001/world/   (returns all queries)
>     * Example Route: http://Your.IP.Address:8001/world/{id}
>   * Nobel Tutorial
>     * Sqlzoo Problem Set: https://sqlzoo.net/wiki/SELECT_from_Nobel_Tutorial
>     * Route Name : nobel
>     * Example Route: http://Your.IP.Address:8001/nobel/   (returns all queries)
>     * Example Route: http://Your.IP.Address:8001/nobel/{id}
>   * Select Within Tutorial
>     * Sqlzoo Problem Set: https://sqlzoo.net/wiki/SELECT_within_SELECT_Tutorial
>     * Route Name : within
>     * Example Route: http://Your.IP.Address:8001/within/    (returns all queries)
>     * Example Route: http://Your.IP.Address:8001/within/{id}
>   * Sum and Count 
>     * Sqlzoo Problem Set: https://sqlzoo.net/wiki/SUM_and_COUNT
>     * Route Name : aggregate
>     * Example Route: http://Your.IP.Address:8001/aggregate/   (returns all queries)
>     * Example Route: http://Your.IP.Address:8001/aggregate/{id}
>   * Join operations
>     * Sqlzoo Problem Set: https://sqlzoo.net/wiki/The_JOIN_operation
>     * Route Name : joins
>     * Example Route: http://Your.IP.Address:8001/joins/   (returns all queries)
>     * Example Route: http://Your.IP.Address:8001/joins/{id}
>   * All
>     * Sqlzoo Problem Set: All of them
>     * Route Name : all
>     * Example Route: http://Your.IP.Address:8001/all
>     * Returns ALL of the previous routes with all id's
  

## Group Projects

### A05: Movie Debacle
  - Should have a visual schema 
  - Discuss design and normalization decisions
  - Api running on port 8002

#### Routes
>
>- Movies 
>  - Find all
>  - Filter on (any field in table)[year,runtime(min/max)]
>    - e.g. return all movies in 1961
>    - e.g. return all movies with runtime > 90
>    - e.g. return all movies with runtime between 80 and 100
>  - Filter on actor or actress (id)
>    - e.g. return all movies associated with a specific actress
>    - e.g. return all movies associated with a set of actors and actresses
>  - Filter on genre(s)
>    - e.g return all movies in a specified genre
>- People
>  - Find all
>  - Filter on name (first or last)
>  - Filter on movie (id)
>  - Filter on genre(s)
>  - Filter on "worked with `id` or `ids`" 
>    - e.g. find all actors and actresses that worked with `id`
>  - Filter on profession
>- Genre
>  - Find all
>- Profession
>  - Find all

-----------

### A06: Restaurant Debacle
  - Should have a visual schema 
  - Discuss design and normalization decisions
  - Api running on port 8002

#### Routes

**Minimum routes** 
- Find all restaurants (paginated result)
- Find unique restaurant categories
- Find all restaurants in a category
- Find all restaurants in a list of 1 or more zip codes
- Find all restaurants near Point(x,y)
- Find all restaurants with a min rating of X

-----------

### A07: Advising Project

- Presentation showing completed project
- Refer to [A07](../A07/README.md)

-----------

### A08: Redis Project

- TBD

------------

### Forever by Daniel

```
Daniel Bowen
How to get API up and running using npm’s FOREVER
1. Install NPM on your droplet - “sudo apt-get install npm”
2. Install Forever - “sudo npm install forever -g”
3. Import uvicorn to the top of your main.py “Import uvicorn”
4. And your main function should include the following 
if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
5. Navigate to your API directory folder, and run Forever using this
	“sudo forever start -c python3 main.py”
A few notes: Any code updates you make won’t be reflected until you kill and restart the forever script. It will keep running unless you explicitly kill the command with the following command “sudo forever stopall”
```