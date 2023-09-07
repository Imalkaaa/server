import http.server
import socketserver
import subprocess
import urllib.parse

PORT = 2728

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        if self.path == '/process':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            query = urllib.parse.parse_qs(post_data)
            user_name = query['name'][0]

            php_script_output = self.run_php_script(user_name)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<!DOCTYPE html><html><body>')
            self.wfile.write(f'<h1>Hello, {user_name}!</h1>'.encode('utf-8'))
            self.wfile.write(f'<p>PHP Output:</p><pre>{php_script_output}</pre>'.encode('utf-8'))
            self.wfile.write(b'</body></html>')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def run_php_script(self, user_name):
        php_script = f'php -r "$html_content = \'Hello, {user_name}!\'; include(\'php_script.php\');"'
        try:
            php_output = subprocess.check_output(php_script, shell=True)
            return php_output.decode('utf-8')
        except subprocess.CalledProcessError as e:
            return f'Error: {e}'

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

