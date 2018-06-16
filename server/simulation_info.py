from datetime import datetime
from dateutil.parser import parse

import pymysql
import ast
import os

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWD = 'Yrtphe1820-='
DB_NAME = 'traffic'
DB_CHARSET = 'utf8mb4'

class simulation_info_db(object):
    def backup_database(self):    

        # Driectory Path
        DIRECTORY_BASE = "C:/shana4/python/backup/"

        file_name = DB_NAME + ".sql"

        execute_command = "mysqldump -h%s -u%s -p%s %s > %s" %(DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DIRECTORY_BASE + '/' + file_name)

        if os.system(execute_command) == 0:
            print("%s backup is complete!" ,DB_NAME)
        else:
            print("Sorry! %s is Backup Failed" ,DB_NAME)
    def create_simulation_info_table (self):
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
                sql = "CREATE TABLE simulation_info (id int NOT NULL, name varchar(20) , duration int, cars_per_second int, vehicle_info text, PRIMARY KEY (id))"
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

    def add_simulation_info (self, simulation_info):
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
                sql = "SELECT MAX(id) FROM `simulation_info`"
                cursor.execute(sql, ())
            
                result = cursor.fetchone()
                if result['MAX(id)'] is None:
                    result['MAX(id)'] = 0
                i = 0
                print(result)
               
                
                # Create a new record
                sql = "INSERT INTO `simulation_info` (`id`,`name`,`duration`,`cars_per_second`,`vehicle_info`) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(sql, (result['MAX(id)']+1, simulation_info['name'],simulation_info['duration'], simulation_info['cars_per_second'],str(simulation_info['vehicle_info'])))
                vidio_id = result['MAX(id)']+1
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
            self.backup_database()
        
        finally:
            connection.close()
        return vidio_id
    
    def serch_all_simulation_info (self):
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
                sql = "SELECT * FROM `simulation_info`"
                cursor.execute(sql)
                result = cursor.fetchall()
               


                
            
        finally:
            connection.close()
        return result
    
    def delete_simulation_info (self, id):
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
                sql = "DELETE FROM `simulation_info` WHERE `id`=%s"
                cursor.execute(sql, (id))
                connection.commit()
                
           
            
        finally:
            connection.close()
        return 