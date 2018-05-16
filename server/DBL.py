from datetime import datetime
from dateutil.parser import parse
import pandas as pd
import pymysql
import junction_db
import simulation_info
import vidio_info_db
import storage_layer
import json

import os
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWD = '123456'
DB_NAME = 'traffic'
DB_CHARSET = 'utf8mb4'
FRAMES_JUMPS_ON_SEARCH = 16
storage = storage_layer.Storage()
vidio_db = vidio_info_db.vidio_info_db()
junction_db = junction_db.junction_info_db()
simulation_db = simulation_info.simulation_info_db()

def search_data(junction_id, meta_key, meta_value):
    storage = storage_layer.Storage()
    dataset = storage.get_all_dataset_files(junction_id)
    ans = []
    for frames in dataset:
        for frame in frames[2]:
            for vehicle in frame["objects"]:
                if vehicle[meta_key] == meta_value:
                    ans.append([vehicle["tracking_id"], frame["frame_index"], frames[1], frames[0]])
    return ans



class DB_Layer(object):
    def __init__(self):
        self.check_tables()

    def empty_all_tables(self):
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
                sql = "DELETE FROM junction_info"
                cursor.execute(sql)
                sql = "DELETE FROM vidio_info"
                cursor.execute(sql)
                sql = "DELETE FROM simulation_info"
                cursor.execute(sql)
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            
        finally:
            connection.close()
        return    

    def drop_all_tables(self):
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
                sql = "DROP table junction_info"
                cursor.execute(sql)
                sql = "DROP table vidio_info"
                cursor.execute(sql)
                sql = "DROP table simulation_info"
                cursor.execute(sql)
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            
        finally:
            connection.close()
        return 

    def check_table_exists(self, tablename):
        is_exist = False
       
        connection = pymysql.connect(host=DB_HOST,
                                    user=DB_USER,
                                    password=DB_PASSWD,
                                    db=DB_NAME,
                                    charset=DB_CHARSET,
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = "SELECT COUNT(*) FROM information_schema.tables WHERE `table_schema` = 'traffic' and `table_name`=%s" 
                cursor.execute(sql, (tablename))
                result = cursor.fetchone()
                
                if result['COUNT(*)'] == 1:
                    is_exist = True
        finally:
            connection.close()
        return is_exist

    def check_tables(self):
        error = False
        try: 
            if not self.check_table_exists('vidio_info'):
                vidio_db.create_vidio_info_table()
            else:
                print('vidio_info exist')
            if not self.check_table_exists('junction_info'):
                junction_db.create_junctions_table()
            else:
                print('junction_info exist')
            if not self.check_table_exists('simulation_info'):
                simulation_db.create_simulation_info_table()
            else:
                print('simulation_info exist')
            print('create table:)')
        except Exception as e:
             error = True
        return error
    def add_junction(self, junction):
        return junction_db.add_row_to_junction_info(junction)
    def get_junctions(self):
        return junction_db.serch_all_junction_info()
    
    def delete_junction(self, junction_id):
        junction_db.delete_junction_info(junction_id)

    def get_datasets(self, junction_id):
        if junction_id==0:
            return simulation_db.serch_all_simulation_info()
        else:
            return vidio_db.serch_vidio_info_by_id_junction(junction_id)
    def add_dataset(self, junction_id, dataset):
        if junction_id==0:
            simulation_db.add_simulation_info(dataset)
        else:
            vidio_db.add_vidio_info(junction_id, dataset)
    def delete_simulation(self, id):
        simulation_db.delete_simulation_info(id)
    
    def delete_vidio_info(self, id):
        vidio_db.delete_vidio_info(id)

    def search_data_min_max(self, junction_id, meta_key, min_meta_value, max_meta_value):
       
        dataset = storage.get_all_dataset_files(junction_id)
        ans = []
        for frames in dataset:
            i = -1
            last = - FRAMES_JUMPS_ON_SEARCH - 2
            for frame in frames[2]:
                i = i + 1
                for vehicle in frame["objects"]:
                    if min_meta_value <= vehicle[meta_key] <= max_meta_value and i > last + FRAMES_JUMPS_ON_SEARCH:
                        res = {
                            'junction_id': junction_id,
                            'dataset_id': frames[0],
                            'vehicle_id': vehicle["tracking_id"],
                            'frame_index': i,
                            'number_of_frames': len(frames[2])
                        }
                        last = i
                        ans.append(res)
        return ans

    def search_data_equal(self, junction_id, meta_key, meta_value):
       
        deta_set = storage.get_all_dataset_files(junction_id)
        ans = []
        for frames in deta_set:
            i = -1
            last = - FRAMES_JUMPS_ON_SEARCH - 2
            for frame in frames[2]:
                i = i + 1
                for vehicle in frame["objects"]:
                    if vehicle[meta_key] == meta_value and i > last + FRAMES_JUMPS_ON_SEARCH:
                        res = {
                            'junction_id': junction_id,
                            'dataset_id': frames[0],
                            'vehicle_id': vehicle["tracking_id"],
                            'frame_index': i,
                            'number_of_frames': len(frames[2])
                        }
                        last = i
                        ans.append(res)
        return ans

    def search_data_min_max_with_dataset(self, junction_id, dataset_id, meta_key, min_meta_value, max_meta_value):
        
        deta_set = storage.get_dataset_files(junction_id, dataset_id)
        ans = []
        for frames in deta_set:
            i = -1
            last = - FRAMES_JUMPS_ON_SEARCH - 2
            for frame in frames:
                i = i + 1
                for vehicle in frame["objects"]:
                    if min_meta_value <= vehicle[meta_key] <= max_meta_value and i > last + FRAMES_JUMPS_ON_SEARCH:
                        res = {
                            'junction_id': junction_id,
                            'dataset_id': dataset_id,
                            'vehicle_id': vehicle["tracking_id"],
                            'frame_index': i,
                            'number_of_frames': len(frames)
                        }
                        last = i
                        ans.append(res)
        return ans

    def search_data_equal_with_dataset(self, junction_id, dataset_id, meta_key, meta_value):
        
        deta_set = storage.get_dataset_files(junction_id, dataset_id)
        ans = []
        for frames in deta_set:
            i = -1
            last = - FRAMES_JUMPS_ON_SEARCH - 2
            for frame in frames:
                i = i + 1
                for vehicle in frame["objects"]:
                    if vehicle[meta_key] == meta_value and i > last + FRAMES_JUMPS_ON_SEARCH:
                        res = {
                            'junction_id': junction_id,
                            'dataset_id': dataset_id,
                            'vehicle_id': vehicle["tracking_id"],
                            'frame_index': i,
                            'number_of_frames': len(frames)
                        }
                        last = i
                        ans.append(res)
        return ans

    def get_dataset_files(self,junction_id,vidio_info_id):
        return storage.get_dataset_files(junction_id, vidio_info_id)

    def store_dataset_file(self,junction_id, vidio_info_id, index, file_content):
        storage.store_dataset_file(junction_id, vidio_info_id, index, file_content)
        
    def delete_junction (self,junction_id):
        storage.delete_junction(junction_id) 

   
    


    