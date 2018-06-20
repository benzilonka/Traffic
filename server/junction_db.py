from datetime import datetime
from dateutil.parser import parse

import pymysql

import os

DB_HOST = 'traffic.c7depggisrds.eu-west-1.rds.amazonaws.com'
DB_USER = 'root'
DB_PASSWD = 'Yrtphe1820-='
DB_NAME = 'traffic'
DB_CHARSET = 'utf8mb4'

class junction_info_db(object):
    def backup_database(self):    

        # Driectory Path
        DIRECTORY_BASE = "C:/shana4/python/backup/"

        file_name = DB_NAME + ".sql"

        execute_command = "mysqldump -h%s -u%s -p%s %s > %s" %(DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DIRECTORY_BASE + '/' + file_name)

        if os.system(execute_command) == 0:
            print("%s backup is complete!" ,DB_NAME)
        else:
            print("Sorry! %s is Backup Failed" ,DB_NAME)
    def create_junctions_table (self):
        # Connect to the database
        connection = pymysql.connect(host=DB_HOST,
                                    user=DB_USER,
                                    password=DB_PASSWD,
                                    db=DB_NAME,
                                    charset=DB_CHARSET,
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "CREATE TABLE junction_info (id int NOT NULL, name varchar(20), lat float, lng float, PRIMARY KEY (id))"
                cursor.execute(sql)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            with connection.cursor() as cursor:
                # Read a single record
                sql = "show tables"
                cursor.execute(sql)
                results = cursor.fetchall()
                for result in results:
                    print(result)
        finally:
            connection.close()
        return

    def add_row_to_junction_info (self,junction):
        # Connect to the database
        connection = pymysql.connect(host=DB_HOST,
                                    user=DB_USER,
                                    password=DB_PASSWD,
                                    db=DB_NAME,
                                    charset=DB_CHARSET,
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = "SELECT MAX(id) FROM `junction_info`"
                cursor.execute(sql, ())
            
                result = cursor.fetchone()
                if result['MAX(id)'] is None:
                    result['MAX(id)'] = 0
                i = 0

                
                # Create a new record
                sql = "INSERT INTO `junction_info` (`id`, `name`, `lat`, `lng`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (result['MAX(id)']+1, junction["name"], junction["lat"], junction["lon"]))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
            self.backup_database()
        
        finally:
            connection.close()
        return result['MAX(id)']+1

    def serch_junction_info_by_id (self,id):
        # Connect to the database
        connection = pymysql.connect(host=DB_HOST,
                                    user=DB_USER,
                                    password=DB_PASSWD,
                                    db=DB_NAME,
                                    charset=DB_CHARSET,
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
       

            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `junction_info` WHERE `id`=%s"
                cursor.execute(sql, (id))
            
                result = cursor.fetchone()

                
            
        finally:
            connection.close()
        return result

    def serch_all_junction_info (self):
        # Connect to the database
        connection = pymysql.connect(host=DB_HOST,
                                    user=DB_USER,
                                    password=DB_PASSWD,
                                    db=DB_NAME,
                                    charset=DB_CHARSET,
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
       

            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `junction_info`"
                cursor.execute(sql, ())
            
                result = cursor.fetchall()

                
            
        finally:
            connection.close()
        return result

    def delete_junction_info (self,id):
        # Connect to the database
        connection = pymysql.connect(host=DB_HOST,
                                    user=DB_USER,
                                    password=DB_PASSWD,
                                    db=DB_NAME,
                                    charset=DB_CHARSET,
                                    cursorclass=pymysql.cursors.DictCursor)
        try:
       

            with connection.cursor() as cursor:
                # Read a single record
                sql = "DELETE FROM `junction_info` WHERE `id`=%s"
                cursor.execute(sql, (id))
                connection.commit()
                self.backup_database()
           
            
        finally:
            connection.close()
        return 