#!/usr/bin/env python3
"""
Soutk Online Compiler - Backend Server
Serves the frontend and executes Soutk code via API.
"""

import http.server
import json
import sys
import os
import threading
import io
from contextlib import redirect_stdout
from urllib.parse import urlparse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from soutk_interpreter import SoutkInterpreter


class SoutkHTTPHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for Soutk compiler server"""
    
    interpreter = None
    
    @classmethod
    def get_interpreter(cls):
        if cls.interpreter is None:
            cls.interpreter = SoutkInterpreter()
        return cls.interpreter
    
    def do_GET(self):
        """Serve static files"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        if path == '/' or path == '/index.html':
            filepath = os.path.join(base_dir, 'index.html')
            self.serve_file(filepath, 'text/html')
        elif path == '/src/soutk_interpreter.py':
            filepath = os.path.join(base_dir, '..', 'src', 'soutk_interpreter.py')
            self.serve_file(filepath, 'text/plain')
        elif path.endswith('.css'):
            filepath = os.path.join(base_dir, path.lstrip('/'))
            self.serve_file(filepath, 'text/css')
        elif path.endswith('.js'):
            filepath = os.path.join(base_dir, path.lstrip('/'))
            self.serve_file(filepath, 'application/javascript')
        else:
            self.send_error(404, 'Not found')
    
    def do_POST(self):
        """Handle code execution API"""
        if self.path == '/api/run':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                code = data.get('code', '')
                
                result = self.run_soutk(code)
                
                self.send_json_response({
                    'success': result['success'],
                    'output': result['output'],
                    'error': result['error']
                })
            except Exception as e:
                self.send_json_response({
                    'success': False,
                    'output': '',
                    'error': str(e)
                })
        else:
            self.send_error(404)
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def serve_file(self, filepath, content_type):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404)
        except Exception as e:
            self.send_error(500, str(e))
    
    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def run_soutk(self, code):
        """Execute Soutk code and capture output"""
        output_lines = []
        
        class OutputCapture:
            def write(self, text):
                output_lines.append(text)
            def flush(self):
                pass
        
        try:
            interpreter = SoutkInterpreter()
            old_stdout = sys.stdout
            error_msg = ''
            
            # Redirect stdout
            sys.stdout = OutputCapture()
            
            # Preprocess code: split by newlines AND semicolons
            processed_code = code.replace(';', '\n')
            
            try:
                interpreter.execute(processed_code)
            except Exception as e:
                error_msg = str(e)
            finally:
                sys.stdout = old_stdout
            
            output = ''.join(output_lines)
            if output.endswith('\n'):
                output = output[:-1]
            
            return {
                'success': (error_msg == ''),
                'output': output,
                'error': error_msg
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e)
            }
    
    def log_message(self, format, *args):
        pass


def run_server(port=8080, open_browser=True):
    """Start the compiler server"""
    server = http.server.HTTPServer(('0.0.0.0', port), SoutkHTTPHandler)
    url = f'http://localhost:{port}'
    
    print(f"\n{'='*50}")
    print(f"  Soutk Online Compiler Server")
    print(f"{'='*50}")
    print(f"  Server running at: {url}")
    print(f"  Press Ctrl+C to stop")
    print(f"{'='*50}\n")
    
    if open_browser:
        def _open():
            import time
            time.sleep(0.8)
            webbrowser.open(url)
        threading.Thread(target=_open, daemon=True).start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.shutdown()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Soutk Online Compiler Server')
    parser.add_argument('--port', type=int, default=8080, help='Port number (default: 8080)')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser automatically')
    args = parser.parse_args()
    
    run_server(args.port, not args.no_browser)
