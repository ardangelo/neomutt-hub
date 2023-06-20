import http.server
import socketserver
import subprocess
import sys

ENDPOINT = sys.argv[1]
COMMAND = sys.argv[2].split()

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == ENDPOINT:
            try:
                # Run the offlineimap command
                output = subprocess.check_output(COMMAND)
                status = 'Success'
            except subprocess.CalledProcessError as e:
                output = str(e.output)
                status = 'Failure'

            # Set the response headers
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            # Set the response body
            response = '{}\n{}'.format(status, output)
            self.wfile.write(response.encode())
        else:
            # Handle other requests with default behavior
            super().do_GET()

# Set up the server
PORT = 4000
Handler = MyRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

# Start the server
print("Server listening on internal port", PORT)
httpd.serve_forever()
