# main.py

from mysqlCnx import MysqlCnx
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import json

##### NEW STUFF #######
# open the config file file and read it
with open('.config.json') as f:
    config = json.loads(f.read())

cnx = MysqlCnx(**config)

class Tut(BaseModel):
    id: int
    title: str
    author: str
    submission_date: str

#####################################################

class Item(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    price: float
    brand: str

def runQuery(group,item_id=None):
    sql = f"SELECT * FROM sql_zoo where `group` = '{group}'"
    if id:
        sql += f" and `id` = '{item_id}'"

    res = cnx.query(sql)
    return res

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/")
async def read_item():
    return {"ids": [1,2,3,4,5,6,7]}  

@app.get("/items/{item_id}")
async def read_item(item_id:int):
    return {"item_id": item_id}

@app.post("/items/")
async def create_item(item: Item):
    jitem = json.loads(item)
    jitem['type']='post'
    return json.dumps(jitem)

@app.put("/items/")
async def create_item(item: Item):
    jitem = json.loads(item)
    jitem['type']='put'
    return json.dumps(jitem)

@app.get("/basics/")
async def read_item():
     # run stuff here
    return {"runs all sql": [1,2,3]} 


#####################
# I added those below.
#####################

@app.get("/world/")
async def read_item():
     # run stuff here
    return {"runs all sql": [1,2,3,4,5,6,7,8,9,10,11,12,13]}  


@app.get("/nobel/")
async def read_item():
     # run stuff here
    return {"runs all sql": [1,2,3,4,5,6,7,8,9,10,11,12,13,14]} 


@app.get("/select/")
async def read_item():
     # run stuff here
    return {"runs all sql": [1,2,3,4,5,6,7,8,9,10]} 


@app.get("/sum and count/")
async def read_item():
     # run stuff here
    return {"runs all sql": [1,2,3,4,5,6,7,8]} 


@app.get("/join/")
async def read_item():
     # run stuff here
    return {"runs all sql": [1,2,3,4,5,6,7,8,9,10,11,12,13]} 


##### NEW STUFF BELOW ######
# @app.get("/basics/{item_id}")
# async def read_item(item_id:int):
#     sql = basics[item_id]['sql']
    
#     response = {
#         'question':basics[item_id]['question'],
#         'sql':basics[item_id]['sql']
#     }

#     res = cnx.query(basics[item_id]['sql'])

#     if res['success']:
#         response['results']=res['data']


#     return response

@app.get("/basics/{item_id}")
async def read_item(item_id:int):
    res = cnx.query(f"SELECT * FROM sql_zoo where `group` = 'basics' and `id` = '{item_id}'")

    sql = res['data'][0]['sql']
    question = res['data'][0]['question']


    res = cnx.query(sql)

    response = {
        'result':res['data'],
        'question':question,
        'sql':sql
    }


    return response



##########################
# Added those below again.
##########################

@app.get("/world/")
async def read_item():
    sql = f"SELECT * FROM sql_zoo where `group` = 'world'"
    print(sql)
    res = cnx.query(sql)

    sql = res['data'][0]['sql']
    question = res['data'][0]['question']


    res = cnx.query(sql)

    response = {
        'result':res['data'],
        'question':question,
        'sql':sql
    }


    return response

@app.get("/world/{item_id}")
async def read_item(item_id:int):
    sql = f"SELECT * FROM sql_zoo where `group` = 'world' and `id` = '{item_id}'"
    print(sql)
    res = cnx.query(sql)

    sql = res['data'][0]['sql']
    question = res['data'][0]['question']


    res = cnx.query(sql)

    response = {
        'result':res['data'],
        'question':question,
        'sql':sql
    }


    return response



@app.get("/nobel/{item_id}")
async def read_item(item_id:int):
    sql = f"SELECT * FROM sql_zoo where `group` = 'nobel' and `id` = '{item_id}'"
    print(sql)
    res = cnx.query(sql)

    sql = res['data'][0]['sql']
    question = res['data'][0]['question']


    res = cnx.query(sql)

    response = {
        'result':res['data'],
        'question':question,
        'sql':sql
    }


    return response



@app.get("/select/{item_id}")
async def read_item(item_id:int):
    sql = f"SELECT * FROM sql_zoo where `group` = 'select' and `id` = '{item_id}'"
    print(sql)
    res = cnx.query(sql)

    sql = res['data'][0]['sql']
    question = res['data'][0]['question']


    res = cnx.query(sql)

    response = {
        'result':res['data'],
        'question':question,
        'sql':sql
    }


    return response



@app.get("/sum_and_count/{item_id}")
async def read_item(item_id:int):
    res = cnx.query(f"SELECT * FROM sql_zoo where `group` = 'sum and count' and `id` = '{item_id}'")

    sql = res['data'][0]['sql']
    question = res['data'][0]['question']


    res = cnx.query(sql)

    response = {
        'result':res['data'],
        'question':question,
        'sql':sql
    }


    return response



@app.get("/join/{item_id}")
async def read_item(item_id:int):
    res = cnx.query(f"SELECT * FROM sql_zoo where `group` = 'join' and `id` = '{item_id}'")

    sql = res['data'][0]['sql']
    question = res['data'][0]['question']


    res = cnx.query(sql)

    response = {
        'result':res['data'],
        'question':question,
        'sql':sql
    }


    return response

# Post route we call from postman
# Tut is defined above by pydantic
# Item is the variable that gets passed to this method
@app.post("/basics/")
async def read_item(item:Tut):
    
    # prints go to console for debugging
    print(item.id)
    
    # build queryn using "item" concatenating both lines using += 
    sql =  f"INSERT INTO `tuts` (`id`, `title`, `author`, `submission_date`) "
    sql += f"VALUES ('{item.id}', '{item.title}', '{item.author}', '{item.submission_date}');"

    # run the query
    res = cnx.query(sql)

    # result has a few entries when it comes back, success is true if everything worked
    # otherwise oops

    # if statement just as example
    # if res['success']:
    #     return res
    # else:
    #     return {'message':'oops'}

    # result has info for a successful query or failed query
    return res 


@app.get("/tuts/")
async def read_item():
    res = cnx.query("SELECT * FROM tuts;")
    return res



@app.get("/tuts/{item_id}")
async def read_item(item_id:int):
    sql = f"""
    SELECT * 
    FROM `tuts`
    WHERE `id` = '{item_id}'
    """
    res = cnx.query(sql)
    return res

@app.post("/tuts/")
async def create_item(item:Tut):
    sql = f"""
    INSERT INTO `tuts` (`id`, `title`, `author`, `submission_date`)
    VALUES ('{item.id}', '{item.title}', '{item.author}', '{item.submission_date}')
    """
    res = cnx.query(sql)
    return res