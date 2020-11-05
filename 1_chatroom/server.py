from http.server import BaseHTTPRequestHandler, HTTPServer

def start_server():
    port = 8080
    server = HTTPServer(('localhost', port), Handler)
    print('Server is running on port', port)
    server.serve_forever()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == 'join':
            pass
        if self.path == 'send':
            pass

    def do_POST(self):
        print('post')

if __name__ == "__main__":
    start_server()