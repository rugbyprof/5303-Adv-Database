import pymongo
from getpass import getpass

client = pymongo.MongoClient('localhost', username='adminguru', password=getpass('Password: '), authMechanism='SCRAM-SHA-256')

db = client.workplace

employees = db.employees

