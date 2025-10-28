from http.server import HTTPServer, BaseHTTPRequestHandler


HTML_PAGE = """\
<html>
  <body>
    <form action="/cgi-bin/range.py" method = "POST">
      <input type="range" name = "Brightness_Level" min = "0" max = "100"
      value = "50"/><br>
      <input type= "submit" value = "Submit">
    </form>

    Select LED:
    <form action="/cgi-bin/radio.py" method = "POST">
      <input type="radio" name = "LED" value = "LED 1" checked > LED 1 <br>
      <input type="radio" name = "LED" value = "LED 2"> <br>
      <input type="radio" name = "LED" value = "LED 3"> <br>
      <input type="submit" value = "Submit">
    </form>
    
    <form action="/" method = "POST">
      <button name= "Change_Brightness" value = b1> Change Brightness </button>
    </form>
  </body>
</html>
"""

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle GET requests (e.g. browser visiting the page)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        # Placeholder function call or message
        response = "GET request received"
        self.wfile.write(response.encode())

    def do_POST(self):
        # Handle POST requests (e.g. form submission or client data)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()

        # Placeholder for your custom function
        print("POST data received:", post_data)

        # Send back a simple confirmation
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        response = "POST request processed"
        self.wfile.write(response.encode())

# Start the HTTP server
if __name__ == "__main__":
    PORT = 8080
    server = HTTPServer(('', PORT), MyHandler)
    print(f"Server running on http://localhost:{PORT}")
    server.serve_forever()
