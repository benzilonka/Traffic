#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from io import BytesIO
import Parser
import DBL

import Sumo_Parser

db = DBL.DB_Layer()


def getFrames(data):
    return Parser.fix_file(data['meta'], json.loads(data['json']))

def getJunctions(data):
    return db.get_junctions()

def getDatasets(data):
    return db.get_datasets(data['junction_id'])

def getDatasetFiles(data):
    return db.get_dataset_files(data['junction_id'], data['dataset_id'])

def addJunction(data):
    return db.add_junction(data['junction'])

def addDataset(data):
    return db.add_dataset(data['junction_id'], data['dataset'])

def addDatasetFile(data):
    file_content = Parser.fix_file(data['meta'], json.loads(data['json']))
    db.store_dataset_file(data['junction_id'], data['dataset_id'], data['index'], file_content)
    return file_content

def deleteJunction(data):
    db.delete_junction(data['junction_id'])
    db.delete_junction(data['junction_id'])
    return True

def createSimulation(data):
    dataset_id = db.add_dataset(0, data['simulation'])
    _jsons = Sumo_Parser.get_simulation(data['simulation']['duration'], data['simulation']['cars_per_second'], data['simulation']['vehicle_info'])
    index = 0
    for _json in _jsons:
        db.store_dataset_file(0, dataset_id, index, _json)
        index = index + 1
    return dataset_id

def getSimulations(data):
    return db.get_datasets(0)

def searchData(data):
    if 'meta_value' in data:        
        if 'dataset_id' in data:
            return db.search_data_equal_with_dataset(data['junction_id'], data['dataset_id'], data['meta_key'], float(data['meta_value']))
        else:
            return db.search_data_equal(data['junction_id'], data['meta_key'], float(data['meta_value']))
    else:
        if 'dataset_id' in data:
            return db.search_data_min_max_with_dataset(data['junction_id'], data['dataset_id'], data['meta_key'], float(data['min_meta_value']), float(data['max_meta_value']))
        else:
            return db.search_data_min_max(data['junction_id'], data['meta_key'], float(data['min_meta_value']), float(data['max_meta_value']))
    

ROUTES = { 
    'getFrames': getFrames,
    'getJunctions': getJunctions,
    'getDatasets': getDatasets,
    'getDatasetFiles': getDatasetFiles,
    'addJunction': addJunction,
    'addDataset': addDataset,
    'addDatasetFile': addDatasetFile,
    'deleteJunction': deleteJunction,
    'createSimulation': createSimulation,
    'getSimulations': getSimulations,
    'searchData': searchData
}

class TrafficServer(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):    
        try:
            print("in post method")
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = json.loads(self.data_string)
            func = ROUTES.get(data['route'], 'unknown_route')
            response = func(data)
            response_str = json.dumps(response)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header("Access-Control-Allow-Origin", "*");
            self.send_header("Access-Control-Expose-Headers", "Access-Control-Allow-Origin");
            self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
            self.end_headers()
            self.wfile.write(response_str.encode())
        except IOError:
            print('404')
            self.send_error(404, 'file not found')
    
def run():
    print('http server is starting...')
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, TrafficServer)
    print('http server is running...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
# with open("big_22.12.2017-10_28_44.json", 'r') as jso:
#     with open("scheduled_11.03.2018-05_24_50.meta", 'r') as meta:
#         a = {'meta': meta.read(), 'json': jso.read()}
#         with open("out.txt", 'w') as outfile:
#             out = getFrames(a)
#             for frame in out:
#                 outfile.write(str(frame))
#                 outfile.write('\n')




