from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
# Serve files from current directory
server_address = ('127.0.0.1', 8000)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
print("Serving on port 8000...")
httpd.serve_forever()
