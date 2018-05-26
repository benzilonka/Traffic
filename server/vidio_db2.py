from datetime import datetime
from dateutil.parser import parse
import pandas as pd
import pymysql

import os

class DB_Layer(object):
    

   

    def backup_database(self):
        
        DB_HOST = 'localhost'
        DB_USER = 'project'
        DB_PASSWD = 'Yrtphe1820-='
        dbname = 'my_project'

        # Driectory Path
        DIRECTORY_BASE = "C:/shana4/python/backup/"

        file_name = dbname + ".sql"

        execute_command = "mysqldump -h%s -u%s -p%s %s > %s" %(DB_HOST, DB_USER, DB_PASSWD, dbname, DIRECTORY_BASE + '/' + file_name)

        if os.system(execute_command) == 0:
            print("%s backup is complete!" ,dbname)
        else:
            print("Sorry! %s is Backup Failed" ,dbname)


    def create_vidio_info_table (self):
    # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "CREATE TABLE vidio_info (id int NOT NULL,junction_id int, name varchar(20), date DATE, PRIMARY KEY (id))"
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

    def create_alert_info_table (self):
                  
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "CREATE TABLE alert_info (file_name varchar(20) NOT NULL, vidio_id int, vidio_direction int NOT NULL, frame_index int NOT NULL, tracking_id int, alert_type varchar(20),alert_date DATE, alert_value float, alert_text text , PRIMARY KEY (file_name, vidio_direction, frame_index, tracking_id, alert_type))"
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
    def add_rows_to_alert_info_info (self,file_name,vidio_id,direction, vidio_info_rows):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                for info_row in vidio_info_rows:
                    objects_info  = info_row['objects']
                    for object_info in objects_info:
                        # Create a new record
                        if(object_info["ttc"]!=-1):
                            sql = "INSERT INTO `alert_info` (`file_name`,`vidio_id`, `vidio_direction`, `frame_index` , `tracking_id`, `alert_type`, `alert_value`,`alert_text`,`alert_date`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                            cursor.execute(sql, (file_name,vidio_id, direction , info_row["frame_index"], object_info["tracking_id"], "ttc",  object_info["ttc"],"",datetime.strptime(object_info['created_at'], '%Y-%m-%d %H:%M:%S.%f')))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
            self.backup_database()
        finally:
            connection.close()
        return
    def serch_by_date_alert_info (self,date_from, date_to):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
       

            with connection.cursor() as cursor:
                # Read a single record
                if date_to is not None:
                    sql = "SELECT * FROM `alert_info` WHERE `alert_date`>=%s and `alert_date`<=%s"
                    cursor.execute(sql, (date_from, date_to))
                else:
                     sql = "SELECT * FROM `alert_info` WHERE `alert_date`>=%s"
                     cursor.execute(sql, (date_from))
                
            
                result = cursor.fetchall()
                
                
        finally:
            connection.close()
        return result
    
    def serch_by_file_name_alert_info (self,file_name):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
       

            with connection.cursor() as cursor:
                # Read a single record
                
                sql = "SELECT * FROM `alert_info` WHERE `file_name`=%s"
                cursor.execute(sql, (file_name))
                
            
                result = cursor.fetchall()

                
        finally:
            connection.close()
        return result

    def serch_all_alert_info (self):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
       

            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `alert_info`"
                cursor.execute(sql, ())
            
                result = cursor.fetchall()

                
        finally:
            connection.close()
        return result
    def delete_by_date_alert_info (self,date_from, date_to):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
       

            with connection.cursor() as cursor:
                # Read a single record
                if date_from is not None:
                    sql = "DELETE FROM `alert_info` WHERE `alert_date`>=%s and `alert_date`<=%s"
                    cursor.execute(sql, (date_from, date_to))
                else:
                     sql = "DELETE FROM `alert_info` WHERE `alert_date`<=%s"
                     cursor.execute(sql, (date_to))
                
            
                connection.commit()
                self.backup_database()
                
        finally:
            connection.close()
        return 
    def create_junctions_table (self):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
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
    def delete_from_all_table (self):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "DELETE FROM junction_info"
                cursor.execute(sql)
                sql = "DELETE FROM vidio_info"
                cursor.execute(sql)
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            
        finally:
            connection.close()
        return
    def add_row_to_junction_info (self,junction):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
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
                cursor.execute(sql, (result['MAX(id)']+1, junction["name"], junction["lat"], junction["lng"]))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
            self.backup_database()
        
        finally:
            connection.close()
        return result['MAX(id)']+1
    def serch_by_id_junction_info (self,id):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
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
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
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

    def delete_by_id_from_junction_info (self,id):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
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
    def add_vidio_num_to_junction (self,id, vidio_id,date_vidio):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
            
                # Create a new record
                sql = "SELECT feeds FROM `junction_info` WHERE `id`=%s"
                cursor.execute(sql, (id))
            
                result = cursor.fetchone()
                sql = """UPDATE junction_info SET feeds=%s WHERE id=%s"""
                cursor.execute (sql,(result['feeds']+','+str(vidio_id)+','+date_vidio, id))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
            self.backup_database()
        
        finally:
            connection.close()
        return

    def update_junction (self,junction):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                list_feeds_info = []
                for feed_info in junction["feeds"]:
                    list_feeds_info.append(str(feed_info['id']))
                    list_feeds_info.append(str(feed_info['date']))
                str_feeds_info = ','.join(list_feeds_info)
                # Create a new record
            
                sql = """UPDATE junction_info SET name=%s, lat=%s, lng=%s, feeds=%s WHERE id=%s"""
                cursor.execute (sql,(junction['name'],junction['lat'],junction['lng'],str_feeds_info,junction['id']))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
            self.backup_database()
        
        finally:
            connection.close()
        return
    
    def add_rows_to_vidio_info (self,junction_id, vidio_info_rows):
        # Connect to the database    
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
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
                name = None
                for key in vidio_info_rows:
                    if(key =='name'):
                        name = vidio_info_rows[key]
                
                # Create a new record
                sql = "INSERT INTO `vidio_info` (`id`,`junction_id`, `name`,`date`) VALUES (%s,%s, %s, %s)"
                cursor.execute(sql, (result['MAX(id)']+1, junction_id, name,datetime.strptime(vidio_info_rows['date'], '%Y-%m-%d %H:%M:%S')))
                vidio_id = result['MAX(id)']+1
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
            self.backup_database()
        
        finally:
            connection.close()
        return vidio_id

    def serch_by_junction_id (self,id):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
       

            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `junction_id` WHERE `id`=%s"
                cursor.execute(sql, (id, vidio_direction))
            
                result = cursor.fetchall()
                

                                
        finally:
            connection.close()
        return result

    def delete_by_vidio_num_and_vidio_direction (self, i):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
       

            with connection.cursor() as cursor:
                # Read a single record
                sql = "DELETE FROM `vidio_info` WHERE `id`=%s"
                cursor.execute(sql, (id, vidio_direction))
                connection.commit()
                self.backup_database()
           
            
        finally:
            connection.close()
        return 
junction = {
    'name': 'ashdod 1',
    'lat': 31.789523,
    'lng': 34.640348,
}
dataset1 = {
    'name' : 'aaaa',
    'date': '2018-04-20 15:15:15'
}
dbl = DB_Layer()
#dbl.create_vidio_info_table()
#dbl.create_junctions_table()
dbl.delete_from_all_table()
num = dbl.add_row_to_junction_info(junction)
num1 = dbl.add_row_to_junction_info(junction)
num2 = dbl.add_rows_to_vidio_info(num,dataset1)
print(num)
print(num1)
print(num2)
print(dbl.serch_by_id_junction_info(num))
print(dbl.serch_all_junction_info())
print(dbl.serch_by_id_junction_info(num))
