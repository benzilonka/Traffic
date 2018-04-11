import pymysql.cursors
class DB_Layer(object):
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
                sql = "CREATE TABLE vidio_info (id int NOT NULL, vidio_direction int NOT NULL, frame_index int NOT NULL, confidence float, type varchar(20), static int , created_at varchar(30), times_lost_by_convnet int, speed float, lost int, alert_tags varchar(500), tracking_id int, bounding_box varchar(200), new int, counted int, PRIMARY KEY (id, vidio_direction, frame_index, tracking_id))"
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
                sql = "CREATE TABLE junction_info (id int NOT NULL, name varchar(20), lat float, lng float, feeds varchar(3000), PRIMARY KEY (id))"
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
                sql = "INSERT INTO `junction_info` (`id`, `name`, `lat`, `lng`, `feeds`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (junction["id"], junction["name"], junction["lat"], junction["lng"], str_feeds_info))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        
        finally:
            connection.close()
        return
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

                junction = {}
                
                junction["id"] = result['id']
                junction["name"] = result['name']
                junction["lat"] = result['lat']
                junction["lng"] = result['lng']
                junction["feeds"] = list()
                lst_feeds = result['feeds'].split(',')
                for i in range(0,len(lst_feeds),2):
                    new_feed = {}
                    new_feed["id"] = int(lst_feeds[i])
                    new_feed["date"] = lst_feeds[i+1]
                    junction["feeds"].append(new_feed)
            
        finally:
            connection.close()
        return junction

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
        
        finally:
            connection.close()
        return
    
    def add_rows_to_vidio_info (self,direction, vidio_info_rows):
        # Connect to the database    
        connection = pymysql.connect(host='localhost',
                                    user='project',
                                    password='123456',
                                    db='my_project',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = "SELECT MAX(id) FROM `vidio_info`"
                cursor.execute(sql, ())
            
                result = cursor.fetchone()
                if result['MAX(id)'] is None:
                    result['MAX(id)'] = 0
                i = 0
                print(result)
                for info_row in vidio_info_rows:
                    objects_info  = info_row['objects']
                    for object_info in objects_info:
                    
                
                        # Create a new record
                        sql = "INSERT INTO `vidio_info` (`id`, `vidio_direction`, `frame_index`, `confidence`, `type`, `static`, `created_at`, `times_lost_by_convnet`, `speed`, `lost`, `alert_tags`, `tracking_id`, `bounding_box`, `new`, `counted`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(sql, (result['MAX(id)']+1, direction, info_row['frame_index'],object_info['confidence'], object_info['type'], object_info['static'], object_info['created_at'], object_info['times_lost_by_convnet'], object_info['speed'], object_info['lost'], ','.join(object_info['alert_tags']), object_info['tracking_id'], ','.join(str(x) for x in object_info['bounding_box']), object_info['new'], object_info['counted']))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        
        finally:
            connection.close()
        return

    def serch_by_vidio_num_and_vidio_direction (self,id, vidio_direction):
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
                sql = "SELECT * FROM `vidio_info` WHERE `id`=%s AND `vidio_direction`=%s"
                cursor.execute(sql, (id, vidio_direction))
            
                result = cursor.fetchall()
                sorted(result, key=lambda x: x['frame_index'])
                prev_index_frame = -1
                frame_list = []
                       

                for row in result:
                    object_info ={}
                    object_info['confidence']   =  row['confidence'] 
                    object_info['type'] = row['type']
                    object_info['static'] = row['static']
                    object_info['created_at'] = row['created_at']
                    object_info['times_lost_by_convnet'] = row['times_lost_by_convnet']
                    object_info['speed'] = row['speed']
                    object_info['lost'] = row['lost']
                    object_info['alert_tags'] = row['alert_tags'].split(',')
                    object_info['tracking_id'] = row['tracking_id']
                    object_info['new'] = row['new']
                    object_info['counted'] = row['counted']            
                    bounding_box = row['bounding_box'].split(',') 
                    object_info['bounding_box'] = list(map(int, bounding_box))
                    if(row['frame_index'] == prev_index_frame):
                   
                        frame_list[len(frame_list)-1]['objects'].append(object_info)
                    else:
                    
                        objects = {'objects' : [object_info], 'frame_index' : row['frame_index']}
                   
                        frame_list.append(objects)
                        prev_index_frame = row['frame_index']

                                
        finally:
            connection.close()
        return frame_list

    def delete_by_vidio_num_and_vidio_direction (self, id, vidio_direction):
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
                sql = "DELETE FROM `vidio_info` WHERE `id`=%s AND `vidio_direction`=%s"
                cursor.execute(sql, (id, vidio_direction))
                connection.commit()
           
            
        finally:
            connection.close()
        return 
junction = {}
junction['id'] = 6
junction['name'] = 'asdod 1'
junction['lat'] = 31.789523
junction['lng'] = 34.640348
junction['feeds'] = list()
feed1 = {}
feed1['id'] = 1
feed1['date'] = '2018/04/10 17:03'
junction['feeds'].append(feed1)
feed2 = {}
feed2['id'] = 2
feed2['date'] = '2018/04/09 10:03'
junction['feeds'].append(feed2)
#add_row_to_junction_info(junction)
dbl = DB_Layer()
print(dbl.serch_by_id_junction_info(6))
print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
dbl.add_vidio_num_to_junction(6,4,"10/10/2012")
print(dbl.serch_by_id_junction_info(6))
print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
junction['name'] = 'gal'
dbl.update_junction(junction)
print(dbl.serch_by_id_junction_info(6))
print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
#delete_by_id_from_junction_info(4)
print('*************************')
#print(serch_by_id_junction_info(3))
frames_info = ({'objects': [{'confidence': 0.8, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 1, 'speed': 9.932450653113678, 'lost': False, 'alert_tags': [], 'tracking_id': 26598, 'bounding_box': [524, 232, 90, 132], 'new': False, 'counted': False}, {'confidence': 0.82, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:02.417256', 'times_lost_by_convnet': 5, 'speed': 7.883500926853487, 'lost': False, 'alert_tags': [], 'tracking_id': 26609, 'bounding_box': [377, 326, 68, 50], 'new': False, 'counted': True}, {'confidence': 0.61, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:03.798450', 'times_lost_by_convnet': 8, 'speed': 6.006274599496227, 'lost': False, 'alert_tags': [], 'tracking_id': 26610, 'bounding_box': [424, 280, 41, 32], 'new': False, 'counted': False}], 'frame_index': 6348724}
,{'objects': [{'confidence': 0.67, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 0, 'speed': 9.404605335094026, 'lost': False, 'alert_tags': [], 'tracking_id': 26598, 'bounding_box': [525, 234, 92, 132], 'new': False, 'counted': False}, {'confidence': 0.82, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:02.417256', 'times_lost_by_convnet': 6, 'speed': 7.46454395779037, 'lost': False, 'alert_tags': [], 'tracking_id': 26609, 'bounding_box': [376, 328, 68, 50], 'new': False, 'counted': True}, {'confidence': 0.61, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:03.798450', 'times_lost_by_convnet': 9, 'speed': 5.687080068679144, 'lost': False, 'alert_tags': [], 'tracking_id': 26610, 'bounding_box': [424, 281, 41, 32], 'new': False, 'counted': False}], 'frame_index': 6348732}
,{'objects': [{'confidence': 0.67, 'type': 'bus', 'static': True, 'created_at': '2017-12-28 07:39:00.933165', 'times_lost_by_convnet': 1, 'speed': 0.0, 'lost': False, 'alert_tags': [], 'tracking_id': 26598, 'bounding_box': [525, 233, 91, 131], 'new': False, 'counted': False}, {'confidence': 0.82, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:02.417256', 'times_lost_by_convnet': 7, 'speed': 6.193790879731843, 'lost': False, 'alert_tags': [], 'tracking_id': 26609, 'bounding_box': [374, 329, 68, 51], 'new': False, 'counted': True}, {'confidence': 0.77, 'type': 'car', 'static': False, 'created_at': '2017-12-28 07:40:03.798450', 'times_lost_by_convnet': 0, 'speed': 18.3427258131377, 'lost': False, 'alert_tags': [], 'tracking_id': 26610, 'bounding_box': [414, 289, 49, 35], 'new': False, 'counted': False}], 'frame_index': 6348741})

#create_vidio_info_table()
dbl.add_rows_to_vidio_info(0, frames_info)
print(dbl.serch_by_vidio_num_and_vidio_direction(1,0))
print('*************************')
dbl.delete_by_vidio_num_and_vidio_direction(1,0)
print(dbl.serch_by_vidio_num_and_vidio_direction(1,0))
