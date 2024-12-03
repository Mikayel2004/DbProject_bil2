import psycopg2
from psycopg2 import sql
from pydbgen import pydbgen
from random import randint
from datetime import date, timedelta, datetime

from DBInit import initDb
from DataGen import dbGen
from config import config

def main():
    try:
        # Step 1: Read database configuration
        print("Reading database configuration...")
        db_params = config()  # Fetch parameters from database.ini

        # Separate admin credentials for database creation
        admin_params = {
            "host": db_params["host"],
            "port": db_params["port"],
            "admin_user": db_params["admin_user"],
            "admin_password": db_params["admin_password"],
            "db_name": db_params["db_name"],
            "db_owner": db_params["db_owner"],
        }

        connection_params = {
            "host": db_params["host"],
            "port": db_params["port"],
            "user": db_params["db_owner"],
            "password": db_params["admin_password"],  # Assume owner uses admin's password
            "dbname": db_params["db_name"],
        }

        # Step 2: Initialize the database
        print("Initializing the database...")
        initDb(
            psycopg2=psycopg2,
            sql=sql,
            host=admin_params["host"],
            port=admin_params["port"],
            admin_user=admin_params["admin_user"],
            admin_password=admin_params["admin_password"],
            db_name=admin_params["db_name"],
            db_owner=admin_params["db_owner"],
        )

        # Step 3: Connect to the initialized database
        print("Connecting to the initialized database...")
        with psycopg2.connect(**connection_params) as connection:
            with connection.cursor() as cursor:
                # Generate and populate data
                print("Populating the database with data...")
                pydb = pydbgen.pydb()
                dbGen(cursor, pydb, randint, date, timedelta, datetime)
                connection.commit()

        print("Database setup and data generation complete!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
