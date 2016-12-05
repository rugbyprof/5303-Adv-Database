from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_restful import reqparse
from flask import jsonify
from flask_cors import CORS, cross_origin

#from pymongo import MongoClient
import pymongo
from bson import Binary, Code
from bson.json_util import dumps
from bson.objectid import ObjectId

import datetime

import json
import urllib


import timeit

app = FlaskAPI(__name__)
CORS(app)

client = pymongo.MongoClient('localhost', 27017)

# change the following to fit your database configuration

db = client['5303DB']   
businessdb = db['yelp.business']
review = db['yelp.review']
userdb = db['yelp.user']
testdb = db['yelp.test']


parser = reqparse.RequestParser()

# ROUTES
"""=================================================================================="""
"""=================================================================================="""
"""=================================================================================="""


@cross_origin() # allow all origins all methods.
@app.route("/", methods=['GET'])
def index():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return func_list

    
"""=================================================================================="""
@app.route("/user/<args>", methods=['GET'])
def user(args):

    args = myParseArgs(args)
    
    if 'skip' in args.keys():
        args['skip'] = int(args['skip'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])

    data = []
    
    #.skip(1).limit(1)
    
    if 'skip' in args.keys() and 'limit' in args.keys():
        result = userdb.find({},{'_id':0}).skip(args['skip']).limit(args['limit'])
    elif 'skip' in args.keys():
        result = userdb.find({},{'_id':0}).skip(args['skip'])
    elif 'limit' in args.keys():
        result = userdb.find({},{'_id':0}).limit(args['limit'])
    else:
        result = userdb.find({},{'_id':0}).limit(10)  

    for row in result:
        data.append(row)


    return {"data":data}
    
"""=================================================================================="""
@app.route("/test/", methods=['POST'])
def test():
    
    data = request.data
    #testdb.insert(request)
    
    return data

@app.route("/<int:key>/", methods=['POST'])
def findkey(key):
    
    data = request.data
    data['key'] = key
    #testdb.insert(request)
    
    return data
    
"""=================================================================================="""
@app.route("/business/<args>", methods=['GET'])
def business(args):

    args = myParseArgs(args)
    
    data = []
    
    result = businessdb.find({},{'_id':0}).limit(100)
    
    for row in result:
        data.append(row)
    

    return {"data":data}
    
# HELPER METHODS
"""=================================================================================="""
"""=================================================================================="""
"""=================================================================================="""

def snap_time(time,snap_val):
    time = int(time)
    m = time % snap_val
    if m < (snap_val // 2):
        time -= m
    else:
        time += (snap_val - m)
        
    if (time + 40) % 100 == 0:
        time += 40
        
    return int(time)

"""=================================================================================="""
def myParseArgs(pairs=None):
    """Parses a url for key value pairs. Not very RESTful.
    Splits on ":"'s first, then "=" signs.
    
    Args:
        pairs: string of key value pairs
        
    Example:
    
        curl -X GET http://cs.mwsu.edu:5000/images/
        

    Returns:
        json object with all images
    """
    
    if not pairs:
        return {}
    
    argsList = pairs.split(":")
    argsDict = {}

    for arg in argsList:
        key,val = arg.split("=")
        argsDict[key]=str(val)
        
    return argsDict
    

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8080)
