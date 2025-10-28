from http.server import HTTPServer, BaseHTTPRequestHandler
import json

HTML_PAGE = """\

<html> 
<body> 
<form action="/cgi-bin/range.py" method="POST"> 
<input type="range" name="Brightness_Level" min="0" max="100" value="50"/><br> 
<input type="submit" value="Submit"> 
</form>
<p>Select LED:</p>
<form action="/cgi-bin/radio.py" method="POST">
  <input type="radio" name="LED" value="LED 1" checked> LED 1 <br>
  <input type="radio" name="LED" value="LED 2"> LED 2 <br>
  <input type="radio" name="LED" value="LED 3"> LED 3 <br>
  <input type="submit" value="Submit">
</form>

<form action="/" method="POST">
  <button name="Change_Brightness" value="b1">Change Brightness</button>
</form>

</body> 
</html>"""

class MyHandler(BaseHTTPRequestHandler):
  def do_GET(self):
# Serve the HTML page at the root
    if self.path == "/" or self.path == "/index.html":
      self.send_response(200)
      self.send_header("Content-type", "text/html")
      self.end_headers()
      self.wfile.write(HTML_PAGE.encode())
    else:
# For any other path, return a simple 404
      self.send_error(404, "File Not Found")

  def do_POST(self):
    # Handle form submissions
    content_length = int(self.headers.get("Content-Length", 0))
    post_data = self.rfile.read(content_length).decode()

    print("POST data received:", post_data)

    # Send a confirmation page back to the browser
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    response = f"""
    <html>
      <body>
        <h2>POST request processed</h2>
        <p>Data received: {post_data}</p>
        <a href="/">Return to main page</a>
      </body>
    </html>
    """
    self.wfile.write(response.encode())


if __name__ == "__main__":

  PORT = 5000
  server = HTTPServer(("127.0.0.1", PORT), MyHandler)
  print(f"Server running on http://localhost:{PORT}")
  server.serve_forever()
