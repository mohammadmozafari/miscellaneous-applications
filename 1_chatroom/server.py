import json
import hashlib
import random as rnd
from http.server import BaseHTTPRequestHandler, HTTPServer

users = {}
encoding = 'utf-8'

def start_server():
    port = 8080
    server = HTTPServer(('localhost', port), Handler)
    print('Server is running on port {}\n'.format(port))
    server.serve_forever()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):        
        if self.path == '/get':
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

if __name__ == "__main__":
    start_server()
