import json
import hashlib
import random as rnd
from threading import Thread, Event, Lock
from http.server import BaseHTTPRequestHandler, HTTPServer

users = {}
encoding = 'utf-8'
waitings = []
message = None

def start_server():
    global message
    port = 8080
    message = Message()
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
            self.get()

    def do_POST(self):
        if self.path == '/join':
            self.join()

        if self.path == '/send':
            self.send()

    # =================================================

    def get(self):
        if self.authenticate():
            sender, msg = message.read()
            self.generate_response(dic={'sender':sender, 'message':msg})
        print('-------------------------------\n')

    def join(self):
        username = self.get_request_body_as_json()['username']
        if username in users.values():
            self.generate_response(403, 'Already exists')
        else:
            token = self.build_token(username)
            users[token] = username
            self.generate_response(200, 'OK', {'token': token})
        print(users)
        print('-------------------------------\n')
    
    def send(self):
        if self.authenticate():
            sender = users[self.headers.get('Sender')]
            msg = self.get_request_body_as_json()['message']
            message.write(msg, sender)
            self.generate_response()
        print('-------------------------------\n')

    # =================================================
    
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

    def authenticate(self):
        if self.headers.get('Sender') not in users.keys():
            self.generate_response(401, 'Unauthorized')
            return False
        return True

class Message():
    def __init__(self):
        self.data = ''
        self.sender = ''
        self.event = Event()
        self.lock = Lock()
        self.event.clear()

    def read(self):
        self.event.wait()
        return self.sender, self.data

    def write(self, data, sender):
        with self.lock:
            self.data = data
            self.sender = sender
            self.event.set()
            self.event.clear()

if __name__ == "__main__":
    start_server()
