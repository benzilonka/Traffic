#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from io import BytesIO

import Clean_Data
#import Parser

def getFrames(meta_file, json_file):
    return Clean_Data.clean(meta_file)


#Create custom HTTPRequestHandler class
class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    #handle POST command
    def do_POST(self):    
        try:
            print("in post method")
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = json.loads(self.data_string)
            func = ROUTES.get(data['route'], 'unknown_route')
            response = func(data['meta'], data['json'])
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

    #ip and port of servr
    #by default http server port is 80
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, KodeFunHTTPRequestHandler)
    print('http server is running...')
    httpd.serve_forever()

ROUTES = { 'getFrames': getFrames }

if __name__ == '__main__':
    run() 
    
    
