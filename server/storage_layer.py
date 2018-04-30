import os
import shutil
import json

STORAGE_DIRECTORY = 'storage'

class Storage():

    def __init__(self):
        if not os.path.exists(STORAGE_DIRECTORY):
            os.makedirs(STORAGE_DIRECTORY)

    def store_dataset_file(self, junction_id, dataset_id, index, file_content):
        try:
            path = '{0}/{1}/{2}'.format(STORAGE_DIRECTORY, junction_id, dataset_id)
            if not os.path.exists(path):
                os.makedirs(path)
            filename = 'dataset_{0}.json'.format(index)
            with open(os.path.join(path, filename), 'w') as temp_file:
                temp_file.write(json.dumps(file_content))
            return True
        except Exception as e:
            print('storage store_dataset_file: Got error {!r}, errno is {}'.format(e, e.args[0]))
            return False

    def get_dataset_files(self, junction_id, dataset_id):
        try:
            path = '{0}/{1}/{2}'.format(STORAGE_DIRECTORY, junction_id, dataset_id)
            if not os.path.exists(path):
                return list()
            res = list()
            for dirname, dirs, files in os.walk(path):
                for filename in files:
                    with open(os.path.join(dirname, filename), 'r') as f:
                        file_content = f.read()                        
                        res.append(json.loads(file_content))
            return res
        except Exception as e:
            print('storage get_dataset_files: Got error {!r}, errno is {}'.format(e, e.args[0]))
            return list()

    def get_all_dataset_files(self, junction_id):
        try:
            path = '{0}/{1}'.format(STORAGE_DIRECTORY, junction_id)
            if not os.path.exists(path):
                return list()
            res = list()
            for dirname, dirs, files in os.walk(path):
                for filename in files:
                    with open(os.path.join(dirname, filename), 'r') as f:
                        file_content = f.read()
                        res.append([dirname.split("\\")[1], filename, json.loads(file_content)])
            return res
        except Exception as e:
            print('storage get_dataset_files: Got error {!r}, errno is {}'.format(e, e.args[0]))
            return list()

    def delete_junction(self, junction_id):
        try:
            shutil.rmtree('{0}/{1}'.format(STORAGE_DIRECTORY, junction_id))
            return True
        except Exception as e:
            print('storage delete_junction: Got error {!r}, errno is {}'.format(e, e.args[0]))
            return False

    def delete_dataset(self, junction_id, dataset_id):
        try:
            shutil.rmtree('{0}/{1}/{2}'.format(STORAGE_DIRECTORY, junction_id, dataset_id))
            return True
        except Exception as e:
            print('storage delete_dataset: Got error {!r}, errno is {}'.format(e, e.args[0]))
            return False