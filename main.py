import psycopg2
from config import config

def connect():
    connection = None
    params = config()
    print("Connecting to db....")
    connection = psycopg2.connect(**params)