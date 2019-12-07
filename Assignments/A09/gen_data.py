#!/usr/local/bin/python3

import pickle
import markovify
import pymongo
from time import sleep
import json
import glob
import os
import random
import datetime
import time
import sys

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["chat"]

def generate_markov_model(directory,file_name):
    """
    Generate a markov model and save the built model in a directory
    using pickle
    """
    # Get raw text as string.
    with open(f"./models/{file_name}") as f:
        text = f.read()

    # Build the model.
    text_model = markovify.Text(text)

    file_name,ext = file_name.split('.')
    path = os.path.join(directory,file_name)
    pickle.dump(text_model,open( f"{path}.p", "wb" ))

def load_saved_markov_models(dir_name):
    """
    I created a few different models 
    """
    model_names = glob.glob(os.path.join(dir_name,"*.p"))
    models = {}
    for mname in model_names:
        name,ext = os.path.basename(mname).split('.')
        models[name] = pickle.load( open( mname, "rb" ) )
    return models



def create_friends():
    """
    Create random friend ships by:
    1) determine how many friends someone should have and generate those
       numbers for all users
    2) loop through users generate a random value between current user and 
       some other user decrementing each users friend count.
    3) continue to end of list 

    Will be easy until most users have thier friend quota and you are trying 
    to match up people who need friends
    """
    mycol = mydb["friends"]



def one_time_load_users(filename):
    """
    Run once to load users into your collection or bucket or node
    """
    mycol = mydb["users"]
    with open(filename) as f:
        json_data = f.read()
        user_data = json.loads(json_data)
    x = mycol.insert_many(user_data)


def load_users_from_DB():
    """
    Load users into one big list just for testing this file
    """
    mycol = mydb["users"]
    users = []
    for u in mycol.find():
        users.append(u)
    return users



if __name__=='__main__':
    #one_time_load_users(f"./data/user_data.json")
    users = load_users_from_DB()
    text_models = load_saved_markov_models("./models")

    # # Print three randomly-generated sentences of no more than 280 characters
    for i in range(100):
        sleep(1)
        user1 = random.choice(users)
        user2 = random.choice(users)
        model = random.choice(list(text_models.keys()))
        from_user = user1['username']
        to_user = user2['username']
        text = text_models[model].make_short_sentence(144)
        now = datetime.datetime.now()
        ts = time.time()    # timestamp to make date math easy
        # formatted timestamp to make reading date easy
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print(f"From:{from_user} To:{to_user} When: {st} \nText:{text}\n")
