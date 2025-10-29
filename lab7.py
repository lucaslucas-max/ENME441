import http.server
import socketserver

led_brightness = [0, 0, 0]

def generate_html():
        """Generate the HTML page with the form and current LED brightness."""
        html = f"""
        <html>
        <head>
        <title>LED Brightness Control</title>
        </head>
        <body>
        <h2>LED Brightness Control</h2>
        <form method="POST">
        <label>Brightness level:</label><br>
        <input type="range" name="brightness" min="0" max="100" value="50"><br><br>

        <label>Select LED:</label><br>
        <input type="radio" name="led" value="0" checked> LED 1 ({led_brightness[0]}%)<br>
        <input type="radio" name="led" value="1"> LED 2 ({led_brightness[1]}%)<br>
        <input type="radio" name="led" value="2"> LED 3 ({led_brightness[2]}%)<br><br>

        <input type="submit" value="Change Brightness">
        </form>

        <h3>Current LED Brightness:</h3>
        <ul>
        <li>LED 1: {led_brightness[0]}%</li>
        <li>LED 2: {led_brightness[1]}%</li>
        <li>LED 3: {led_brightness[2]}%</li>
        </ul>
        </body>
        </html>
        """
        return html

class LEDRequestHandler(http.server.SimpleHTTPRequestHandler):
  def do_GET(self):
    """Serve the HTML page when user opens the site."""
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(generate_html().encode("utf-8"))

def do_POST(self):
    """Handle form submission from the HTML page."""
    # Read raw POST data
    length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(length).decode("utf-8")

    # Manually extract the LED and brightness values
    # Example data: "brightness=75&led=1"
    brightness_value = 0
    led_index = 0

    if "brightness=" in post_data:
        part = post_data.split("brightness=")[1]
        brightness_str = part.split("&")[0]
        if brightness_str.isdigit():
            brightness_value = int(brightness_str)

    if "led=" in post_data:
        led_str = post_data.split("led=")[1]
        if led_str.isdigit():
            led_index = int(led_str)

    # Update LED brightness
    led_brightness[led_index] = brightness_value

    # (In a real setup, this is where you'd send the PWM signal to GPIO)
    print(f"LED {led_index + 1} brightness set to {brightness_value}%")

    # Respond with updated HTML page
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(generate_html().encode("utf-8"))

PORT = 8080
with socketserver.TCPServer(("", PORT), LEDRequestHandler) as httpd:
  print(f"Serving on port {PORT}")
  httpd.serve_forever()
