import pymysql
import storage_layer

DB_HOST='localhost'
DB_USER='root'
DB_PASSWORD='Yrtphe1820-='
DB_NAME='traffic'
DB_PORT=3306
DB_CHARSET='utf8'
DB_TABLES = ['junctions', 'datasets', 'junctions_meta', 'datasets_meta']

class DB():

    def __init__(self):
        self.connectToDB()
    
    def connectToDB(self):
        error=False
        print('connecting to db..')
        try:
            self.dbcon = pymysql.connect(host=DB_HOST,
                                        user=DB_USER,
                                        password=DB_PASSWORD,
                                        db=DB_NAME,
                                        port=DB_PORT,
                                        charset=DB_CHARSET,
                                        autocommit=True,
                                        cursorclass=pymysql.cursors.DictCursor)
            print('success')
        except Exception as e:
            print('__init__: Got error {!r}, errno is {}'.format(e, e.args[0]))
            error = True
        error = self.check_tables() or error
        if error:
            print('db got errored')
        else:
            print('db is ready..')

    def drop_all_tables(self):
        dbcur = self.dbcon.cursor()
        for table in DB_TABLES:
            try:
                query = """
                        DROP TABLE {0}
                    """.format(table)
                dbcur.execute(query)
            except Exception as e:
                print('drop_all_tables: Got error {!r}, errno is {}'.format(e, e.args[0]))
                if(e.args[0] == 2006):
                    self.connectToDB()


    def empty_all_tables(self):
        dbcur = self.dbcon.cursor()
        for table in DB_TABLES:
            try:
                query = """
                        DELETE FROM {0}
                        WHERE 1
                    """.format(table)
                dbcur.execute(query)
            except Exception as e:
                print('empty_all_tables: Got error {!r}, errno is {}'.format(e, e.args[0]))
                if(e.args[0] == 2006):
                    self.connectToDB()


    def check_tables(self):
        error=False
        for table in DB_TABLES:
            try:
                print('checking if {0} table exists'.format(table))
                if not self.check_table_exists(table):
                    print('{0} table does not exists'.format(table))
                    self.create_table(table)
                else:
                    print('{0} table exists'.format(table))
            except Exception as e:
                print('check_tables: Got error {!r}, errno is {}'.format(e, e.args[0]))
                error=True
                if(e.args[0] == 2006):
                    self.connectToDB()
        return error


    def check_table_exists(self, tablename):
        dbcur = self.dbcon.cursor()
        try:
            dbcur.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_name = '{0}'
                """.format(tablename))
            res = dbcur.fetchone()
            if res['COUNT(*)'] == 1:
                return True
        except Exception as e:
            print('check_table_exists: Got error {!r}, errno is {}'.format(e, e.args[0]))
            if(e.args[0] == 2006):
                self.connectToDB()
        return False
    

    def create_table(self, tablename):
        if tablename == DB_TABLES[0]: #junctions 
            query = """
                CREATE TABLE {0} (id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY)
                """
        elif tablename == DB_TABLES[1]: #datasets
            query = """
                CREATE TABLE {0} (id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY, item_id INT(8) UNSIGNED)
                """
        else: #metas
            query = """
                CREATE TABLE {0} (id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
                                  item_id INT(8) UNSIGNED, 
                                  meta_key varchar(32), 
                                  meta_value varchar(50))
                """
        try:
            dbcur = self.dbcon.cursor()
            dbcur.execute(query.format(tablename))
        except Exception as e:
            print('create_table: Got error {!r}, errno is {}'.format(e, e.args[0]))
            if(e.args[0] == 2006):
                self.connectToDB()



    def add_junction(self, junction):
        dbcur = self.dbcon.cursor()
        try:
            query = """
                        INSERT INTO {0}
                        () VALUES ()
                    """.format(DB_TABLES[0])
            dbcur.execute(query)            
            junction_id = dbcur.lastrowid
            for key in junction:
                query = """
                            INSERT INTO {0}
                            (item_id, meta_key, meta_value)
                            VALUES
                            ({1}, '{2}', '{3}')
                        """.format(DB_TABLES[2], junction_id, key, junction[key])
                dbcur.execute(query)
            return junction_id
        except Exception as e:
            print('add_junction: Got error {!r}, errno is {}'.format(e, e.args[0]))
            if(e.args[0] == 2006):
                self.connectToDB()
            return False


    def get_junctions(self):
        dbcur = self.dbcon.cursor()
        junctions = list()
        try:
            query = """
                        SELECT * FROM {0}
                        WHERE 1
                    """.format(DB_TABLES[0])
            dbcur.execute(query)
            junctions_rows = dbcur.fetchall()
            for row in junctions_rows:
                junction = dict()
                for key, value in row.items():
                    junction[key] = value
                query = """
                            SELECT * FROM {0}
                            WHERE item_id = {1}
                        """.format(DB_TABLES[2], junction['id'])
                dbcur.execute(query)
                metas_rows = dbcur.fetchall()
                for meta_row in metas_rows:
                    junction[meta_row['meta_key']] = meta_row['meta_value']
                junctions.append(junction)
        except Exception as e:
            print('get_junctions: Got error {!r}, errno is {}'.format(e, e.args[0]))
            if(e.args[0] == 2006):
                self.connectToDB()
        return junctions


    def delete_junction(self, junction_id):
        dbcur = self.dbcon.cursor()
        try:
            query = """
                        DELETE FROM {0}
                        WHERE id = {1}
                    """.format(DB_TABLES[0], junction_id)
            dbcur.execute(query) #delete from junctions

            query = """
                        DELETE FROM {0}
                        WHERE item_id = {1}
                    """.format(DB_TABLES[2], junction_id)
            dbcur.execute(query) #delete from junctions_meta

            query = """
                        SELECT id FROM {0}
                        WHERE item_id = {1} 
                    """.format(DB_TABLES[1], junction_id)
            dbcur.execute(query) #select datasets
            datasets_rows = dbcur.fetchall()
            for row in datasets_rows:
                dataset_id = row['id']
                query = """
                            DELETE FROM {0}
                            WHERE item_id = {1}
                        """.format(DB_TABLES[3], dataset_id)
                dbcur.execute(query) #delete datasets metas
            query = """
                        DELETE FROM {0}
                        WHERE item_id = {1}
                    """.format(DB_TABLES[1], junction_id)
            dbcur.execute(query) #delete datasets
            return True
        except Exception as e:
            print('delete_junction: Got error {!r}, errno is {}'.format(e, e.args[0]))
            if(e.args[0] == 2006):
                self.connectToDB()
            return False


    def get_datasets(self, junction_id):
        dbcur = self.dbcon.cursor()
        datasets = list()
        try:
            query = """
                        SELECT * FROM {0}
                        WHERE item_id = {1}
                    """.format(DB_TABLES[1], junction_id)
            dbcur.execute(query)
            datasets_rows = dbcur.fetchall()
            for row in datasets_rows:
                dataset = dict()
                for key, value in row.items():
                    dataset[key] = value
                query = """
                            SELECT * FROM {0}
                            WHERE item_id = {1}
                        """.format(DB_TABLES[3], dataset['id'])
                dbcur.execute(query)
                metas_rows = dbcur.fetchall()
                for meta_row in metas_rows:
                    dataset[meta_row['meta_key']] = meta_row['meta_value']
                datasets.append(dataset)
        except Exception as e:
            print('get_datasets: Got error {!r}, errno is {}'.format(e, e.args[0]))            
            if(e.args[0] == 2006):
                self.connectToDB()
        return datasets


    def add_dataset(self, junction_id, dataset):
        dbcur = self.dbcon.cursor()
        try:
            query = """
                        INSERT INTO {0}
                        (item_id) VALUES ({1})
                    """.format(DB_TABLES[1], junction_id)
            dbcur.execute(query)            
            dataset_id = dbcur.lastrowid
            for key in dataset:
                query = """
                            INSERT INTO {0}
                            (item_id, meta_key, meta_value)
                            VALUES
                            ({1}, '{2}', '{3}')
                        """.format(DB_TABLES[3], dataset_id, key, dataset[key])
                dbcur.execute(query)
            return dataset_id
        except Exception as e:
            print('add_dataset: Got error {!r}, errno is {}'.format(e, e.args[0]))
            if(e.args[0] == 2006):
                self.connectToDB()
            return False


    def delete_dataset(self, dataset_id):
        dbcur = self.dbcon.cursor()
        try:
            query = """
                        DELETE FROM {0}
                        WHERE id = {1}
                    """.format(DB_TABLES[1], dataset_id)
            dbcur.execute(query) #delete from datasets

            query = """
                        DELETE FROM {0}
                        WHERE item_id = {1}
                    """.format(DB_TABLES[3], dataset_id)
            dbcur.execute(query) #delete from datasets_meta
            return True
        except Exception as e:
            print('delete_junction: Got error {!r}, errno is {}'.format(e, e.args[0]))
            if(e.args[0] == 2006):
                self.connectToDB()
            return False


'''

db = DB()

junction = {
    'name': 'ashdod 1',
    'lat': 31.789523,
    'lng': 34.640348,
}
dataset1 = {
    'date': '2018-04-20 15:15:15'
}

db.empty_all_tables()



junction_id = db.add_junction(junction)
print(junction_id)

print(db.get_junctions())

dataset1_id = db.add_dataset(junction_id, dataset1)
print(dataset1_id)

print(db.get_datasets(junction_id))


print(db.get_datasets(junction_id))

storage = storage_layer.Storage()

storage.store_dataset_file(junction_id, dataset1_id, 0, 'file_content'.encode())
print(storage.get_dataset_files(junction_id, dataset1_id))

storage.delete_dataset(junction_id, dataset1_id)
print(storage.get_dataset_files(junction_id, dataset1_id))

print(db.delete_junction(junction_id))
print(storage.delete_junction(junction_id))

print(db.get_junctions())

'''