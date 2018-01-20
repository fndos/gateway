from __future__ import print_function
import requests
import grpc
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

import microservice_pb2
import microservice_pb2_grpc

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        dicti = {}
        if (self.path == '/'):
            channel = grpc.insecure_channel('localhost:50051')
            stub = microservice_pb2_grpc.MicroserviceStub(channel)
            for news in stub.ListNews(microservice_pb2.Numero(numero=10)):
                dicti[news.title]=news.url
            jsonresp = json.dumps(dicti)
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(jsonresp.encode())
        elif (self.path == '/justdb'):
            channel = grpc.insecure_channel('localhost:50052')
            stub = microservice_pb2_grpc.MicroserviceStub(channel)
            for news in stub.ListNews(microservice_pb2.Numero(numero=10)):
                dicti[news.title]=news.url
            jsonresp = json.dumps(dicti)
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(jsonresp.encode())
        else:
            self.send_response(200) #cambiar esto luego
        
    

def run():
    server = HTTPServer(('localhost', 9000), Handler)
    print ('Starting server at http://localhost:9000')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown

if __name__ == '__main__':
    run()
