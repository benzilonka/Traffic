from datetime import datetime
from dateutil.parser import parse
import pandas as pd
import pymysql

import os

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWD = '123456'
DB_NAME = 'traffic'
DB_CHARSET = 'utf8mb4'

class vidio_info_db(object):
    def backup_database(self):    

        # Driectory Path
        DIRECTORY_BASE = "C:/shana4/python/backup/"

        file_name = DB_NAME + ".sql"

        execute_command = "mysqldump -h%s -u%s -p%s %s > %s" %(DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DIRECTORY_BASE + '/' + file_name)

        if os.system(execute_command) == 0:
            print("%s backup is complete!" ,DB_NAME)
        else:
            print("Sorry! %s is Backup Failed" ,DB_NAME)
    def create_vidio_info_table (self):
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
                sql = "CREATE TABLE vidio_info (id int NOT NULL,junction_id int, name varchar(20), PRIMARY KEY (id))"
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

    def add_vidio_info (self,junction_id, vidio_info):
        # Connect to the database    
        connection = pymysql.connect(host=DB_HOST,
                                    user=DB_USER,
                                    password=DB_PASSWD,
                                    db=DB_NAME,
                                    charset=DB_CHARSET,
                                    cursorclass=pymysql.cursors.DictCursor)
        vidio_id = -1

        try:
            with connection.cursor() as cursor:
                sql = "SELECT MAX(id) FROM `vidio_info`"
                cursor.execute(sql, ())
            
                result = cursor.fetchone()
                if result['MAX(id)'] is None:
                    result['MAX(id)'] = 0
                i = 0
                print(result)
              
                
                # Create a new record
                sql = "INSERT INTO `vidio_info` (`id`,`junction_id`, `name`) VALUES (%s,%s, %s)"
                cursor.execute(sql, (result['MAX(id)']+1, junction_id,vidio_info['name']))
                vidio_id = result['MAX(id)']+1
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
            self.backup_database()
        
        finally:
            connection.close()
        return vidio_id
    
    def serch_vidio_info_by_id_junction (self,junction_id):
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
                sql = "SELECT * FROM `vidio_info` WHERE `junction_id`=%s"
                cursor.execute(sql, (junction_id))
            
                result = cursor.fetchall()

                
            
        finally:
            connection.close()
        return result
    
    def delete_vidio_info (self, id):
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
                sql = "DELETE FROM `vidio_info` WHERE `id`=%s"
                cursor.execute(sql, (id))
                connection.commit()
                self.backup_database()
           
            
        finally:
            connection.close()
        return 