from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello from CI/CD Pipeline - Build OK')
    def log_message(self, format, *args):
        pass

HTTPServer(('', 8080), Handler).serve_forever()
