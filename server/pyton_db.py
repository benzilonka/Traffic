
import pymysql.cursors
class data_row(object):

   

    def __init__(self, vidio_num, vidio_direction, frame_index, confidence, ob_type, static, created_at, time_losts_by_convert, spead, lost, alert_tag, tracking_id, bounding_x, bounding_y, bounding_width, bounding_high, new, counted):
        self.vidio_num = vidio_num
        self.vidio_direction = vidio_direction
        self.frame_index = frame_index
        self.confidence = confidence
        self.type = ob_type
        self.static = static
        self.created_at = created_at
        self.time_losts_by_convert = time_losts_by_convert
        self.spead = spead
        self.lost = lost
        self.alert_tag = alert_tag
        self.tracking_id = tracking_id
        self.bounding_x = bounding_x
        self.bounding_y = bounding_y
        self.bounding_width = bounding_width
        self.bounding_high = bounding_high
        self.new = new
        self.counted = counted
def create_vidio_info_table ():
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
            sql = "CREATE TABLE vidio_info (vidio_num int NOT NULL, vidio_direction int NOT NULL, frame_index int NOT NULL, confidence float, type varchar(20), static int , created_at varchar(30), time_losts_by_convert int, spead float, lost int, alert_tag varchar(200), tracking_id int, bounding_x int, bounding_y int, bounding_width int, bounding_high int, new int, counted int, PRIMARY KEY (vidio_num, vidio_direction, frame_index))"
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
def add_row_to_db (row_of_data):
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
            sql = "INSERT INTO `vidio_info` (`vidio_num`, `vidio_direction`, `frame_index`, `confidence`, `type`, `static`, `created_at`, `time_losts_by_convert`, `spead`, `lost`, `alert_tag`, `tracking_id`, `bounding_x`, `bounding_y`, `bounding_width`, `bounding_high`, `new`, `counted`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (row_of_data.vidio_num, row_of_data.vidio_direction, row_of_data.frame_index,row_of_data.confidence, row_of_data.type, row_of_data.static, row_of_data.created_at, row_of_data.time_losts_by_convert, row_of_data.spead, row_of_data.lost, row_of_data.alert_tag, row_of_data.tracking_id, row_of_data.bounding_x, row_of_data.bounding_y, row_of_data.bounding_width, row_of_data.bounding_high, row_of_data.new, row_of_data.counted))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
        
    finally:
        connection.close()
    return
def serch_by_vidio_num_and_vidio_direction (vidio_num, vidio_direction):
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
            sql = "SELECT * FROM `vidio_info` WHERE `vidio_num`=%s AND `vidio_direction`=%s"
            cursor.execute(sql, (vidio_num, vidio_direction))
            
            result = cursor.fetchall()
            
    finally:
        connection.close()
    return result

def delete_by_vidio_num_and_vidio_direction (vidio_num, vidio_direction):
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
            sql = "DELETE FROM `vidio_info` WHERE `vidio_num`=%s AND `vidio_direction`=%s"
            cursor.execute(sql, (vidio_num, vidio_direction))
            connection.commit()
           
            
    finally:
        connection.close()
    return 
#create_vidio_info_table()
my_row_1 = data_row(1111, 2, 33, 0.1, 'aaa', 4, 'bbb', 6, 0.1, 7,'ccc', 8, 9, 10, 11, 12, 13, 14)
my_row_2 = data_row(1111, 22, 33, 0.1, 'aaa', 4, 'bbb', 6, 0.1, 7,'ccc', 8, 9, 10, 11, 12, 13, 14)

#print(my_row_2.frame_index)
add_row_to_db(my_row_1)
add_row_to_db(my_row_2)
my_result = serch_by_vidio_num_and_vidio_direction(1111,22)

for row in my_result:
    print(row)
my_result = delete_by_vidio_num_and_vidio_direction(1111,22)
my_result = serch_by_vidio_num_and_vidio_direction(1111,22)

for row in my_result:
    print(row)
