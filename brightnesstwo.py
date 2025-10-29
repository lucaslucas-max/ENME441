from http.server import HTTPServer, BaseHTTPRequestHandler
import json

HTML_PAGE = """\
<!DOCTYPE html>
<html>
<head>
  <title>LED Brightness Control</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      text-align: center;
      margin-top: 50px;
    }
    .slider-container {
      display: inline-block;
      text-align: left;
      border: 2px solid #333;
      border-radius: 10px;
      padding: 20px;
    }
    .slider {
      width: 200px;
      margin: 10px;
    }
  </style>
</head>
<body>
  <div class="slider-container">
    <div>
      LED1: <input type="range" min="0" max="100" value="50" class="slider" id="led1">
      <span id="val1">50</span>
    </div>
    <div>
      LED2: <input type="range" min="0" max="100" value="50" class="slider" id="led2">
      <span id="val2">50</span>
    </div>
    <div>
      LED3: <input type="range" min="0" max="100" value="50" class="slider" id="led3">
      <span id="val3">50</span>
    </div>
  </div>

  <script>
    function sendBrightness(led, value) {
      fetch('/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({led: led, brightness: value})
      })
      .then(response => response.text())
      .then(data => console.log(data))
      .catch(error => console.error('Error:', error));
    }

    const sliders = ['led1', 'led2', 'led3'];

    sliders.forEach((id, index) => {
      const slider = document.getElementById(id);
      const display = document.getElementById('val' + (index + 1));

      slider.addEventListener('input', () => {
        const value = slider.value;
        display.textContent = value;
        sendBrightness(id.toUpperCase(), value);
      });
    });
  </script>
</body>
</html>
"""

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode())
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()

        try:
            data = json.loads(post_data)
            led = data.get("led")
            brightness = data.get("brightness")
            print(f"Set {led} brightness to {brightness}")
        except json.JSONDecodeError:
            print("Received non-JSON POST data:", post_data)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Brightness updated")

if __name__ == "__main__":
    PORT = 5000
    server = HTTPServer(('', PORT), MyHandler)
    print(f"Server running on http://localhost:{PORT}")
    server.serve_forever()
