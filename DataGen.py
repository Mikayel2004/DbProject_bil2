def dbGen(cursor, pydb, randint, date, timedelta, datetime):
    try:
        professors = []
        for _ in range(10):
            name = pydb.fake.name()
            degree = pydb.fake.job()
            department = pydb.fake.company_suffix()
            position = pydb.fake.word()
            professors.append((name, degree, department, position))

        cursor.executemany("""
            INSERT INTO professor (name, degree, department, position) 
            VALUES (%s, %s, %s, %s);
        """, professors)

        subjects = []
        for _ in range(20):
            name = pydb.fake.bs()
            hours = randint(10, 40)
            professor_id = randint(1, len(professors))
            subjects.append((name, hours, professor_id))

        cursor.executemany("""
            INSERT INTO subject (name, hours, professor_id) 
            VALUES (%s, %s, %s);
        """, subjects)

        schedules = []
        for _ in range(50):
            subject_id = randint(1, len(subjects))
            schedule_date = date.today() + timedelta(days=randint(1, 30))
            schedule_time = datetime.now().replace(hour=randint(8, 18), minute=0, second=0).time()
            group_name = pydb.fake.word().capitalize()
            schedules.append((subject_id, schedule_date, schedule_time, group_name))

        cursor.executemany("""
            INSERT INTO schedule (subject_id, date, time, group_name) 
            VALUES (%s, %s, %s, %s);
        """, schedules)
        print("Data successfully populated.")
    except Exception as e:
        print("Error in data generation: ", e)
