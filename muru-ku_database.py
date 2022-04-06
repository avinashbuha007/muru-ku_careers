import pymysql as MySQLdb

db_host = 'localhost'
db_user = 'root'
db_password = 'test'
db_name = 'muru_ku_startups'
db_table_name = 'muru_ku_jobs'

connection = MySQLdb.connect(host=db_host,
                      user=db_user,
                      password=db_password,
                      database=db_name,
                      charset='utf8mb4')
cursor = connection.cursor()

def create_database():
    try:
        sql = f"create database if not exists {db_name} default charset utf8mb4 collate utf8mb4_general_ci;"
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        print(e)

def create_table():
    try:
        sql = f"""create table if not exists {db_table_name} (id int(11) not null auto_increment,website_name text,website_url text,career_url text,job_title text,location text,description text,primary key(id)) DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;"""
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        print(e)