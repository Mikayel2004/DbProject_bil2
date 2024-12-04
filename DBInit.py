# DBInit.py

def initDb(psycopg2, sql, host, port, admin_user, admin_password, db_name, db_owner):
    try:
        print("Connecting to PostgreSQL as admin...")
        admin_conn = psycopg2.connect(
            host=host,
            port=port,
            user=admin_user,
            password=admin_password,
            dbname="postgres"
        )
        admin_conn.autocommit = True
        print("Autocommit status:", admin_conn.autocommit)

        with admin_conn.cursor() as admin_cursor:
            print(f"Checking if database '{db_name}' exists...")
            admin_cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
            db_exists = admin_cursor.fetchone()
            if db_exists:
                print(f"Database '{db_name}' already exists. Skipping creation.")
            else:
                print(f"Creating database '{db_name}' with owner '{db_owner}'...")
                admin_cursor.execute(
                    sql.SQL("CREATE DATABASE {db_name} OWNER {owner}")
                    .format(
                        db_name=sql.Identifier(db_name),
                        owner=sql.Identifier(db_owner)
                    )
                )
                print(f"Database '{db_name}' successfully created.")
        admin_conn.close()

        print(f"Connecting to the new database '{db_name}' to initialize tables...")
        with psycopg2.connect(
            host=host,
            port=port,
            user=db_owner,
            password=admin_password,
            dbname=db_name
        ) as db_conn:
            with db_conn.cursor() as cursor:
                print("Creating tables...")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS professor (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        degree VARCHAR(50),
                        department VARCHAR(50),
                        position VARCHAR(50)
                    );
                    CREATE TABLE IF NOT EXISTS subject (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        hours INTEGER NOT NULL,
                        professor_id INTEGER REFERENCES professor(id)
                    );
                    CREATE TABLE IF NOT EXISTS schedule (
                        id SERIAL PRIMARY KEY,
                        subject_id INTEGER REFERENCES subject(id),
                        date DATE NOT NULL,
                        time TIME NOT NULL,
                        group_name VARCHAR(50) NOT NULL
                    );
                """)
                db_conn.commit()
                print("Tables successfully created in the database.")

    except psycopg2.Error as e:
        print(f"Error during database initialization: {e}")
    finally:
        print("Database initialization process completed.")
