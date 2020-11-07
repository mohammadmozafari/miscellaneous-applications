import time
import json
import hashlib
import random as rnd
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

users = {}
encoding = 'utf-8'
waitings = []

def start_server():
    port = 8080
    server = ThreadedHTTPServer(('localhost', port), Handler)
    print('Server is running on port {}\n'.format(port))
    server.serve_forever()

class ThreadedHTTPServer(HTTPServer):
    def process_request(self, request, client_address):
        thread = Thread(target=self.__new_request, args=(
            self.RequestHandlerClass, request, client_address, self))
        thread.start()

    def __new_request(self, handlerClass, request, address, server):
        handlerClass(request, address, server)
        self.shutdown_request(request)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):        
        if self.path == '/get':
            time.sleep(10)
            pass

    def do_POST(self):
        if self.path == '/join':
            username = self.get_request_body_as_json()['username']
            if username in users.values():
                self.generate_response(403, 'Already exists')
            else:
                token = self.build_token(username)
                users[token] = username
                self.generate_response(200, 'OK', {'token': token})
            print(users)
            print('-------------------------------\n')

        if self.path == '/send':
            pass

    def build_token(self, name):
        n1 = rnd.randint(1, 100)
        n2 = rnd.randint(1, 100)
        st = '{}:{}:{}'.format(n1, name, n2)
        result = hashlib.md5(st.encode(encoding)).hexdigest()
        return result

    def generate_response(self, code=200, msg='OK', dic=None):
        self.send_response(code, msg)
        self.end_headers()
        if dic is not None:
            self.wfile.write(json.dumps(dic).encode(encoding))

    def get_request_body_as_json(self):
        msg_size = int(self.headers.get('Content-Length'))
        return json.loads(self.rfile.read(msg_size).decode(encoding))

class Message():
    pass

if __name__ == "__main__":
    start_server()
