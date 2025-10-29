import http.server
import socketserver

led_brightness = [0, 0, 0]

def generate_html():
        """Generate HTML page showing current LED states and brightness form."""
        html = f"""
        <html>
        <head>
        <title>LED Brightness Control</title>
        </head>
        <body>
        <h2>LED Brightness Control</h2>
        <form method="POST">
        <label>Brightness level:</label><br>
        <input type="range" name="brightness" min="0" max="100" value="50">
        <br><br>
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

class LEDRequestHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
                """Serve the HTML form when accessed via browser."""
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(generate_html().encode("utf-8"))

def do_POST(self):
    """Handle form submission and update LED brightness."""
    content_length = int(self.headers["Content-Length"])
    post_data = self.rfile.read(content_length).decode("utf-8")

    # Manually parse form data (no urllib)
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

    # Update stored brightness for the selected LED
    led_brightness[led_index] = brightness_value
    print(f"LED {led_index + 1} brightness set to {brightness_value}%")

    # Send updated HTML page back
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(generate_html().encode("utf-8"))

PORT = 8080
with socketserver.TCPServer(("", PORT), LEDRequestHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()
