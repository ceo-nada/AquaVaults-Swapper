import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from dotenv import load_dotenv

load_dotenv()  # reads .env file into environment variables

class EnvHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/config.js":
            rpc_url = os.getenv("RPC_URL", "https://api.mainnet-beta.solana.com")
            content = f'window.APP_CONFIG = {{ DEFAULT_RPC: "{rpc_url}" }};'
            self.send_response(200)
            self.send_header("Content-type", "application/javascript")
            self.end_headers()
            self.wfile.write(content.encode())
        else:
            super().do_GET()

#print(f"Port: {int(os.getenv("LOCAL_PORT"))}, Type: {type(int(os.getenv("LOCAL_PORT")))}")
port = int(os.getenv("LOCAL_PORT", 8000)) #Use your custom por if defined, otherwise default to 8000 
print(f"🌐 Serving AquaVaults-Swapper on http://localhost:{port}/swapper-ui.html")
print(f"Using Custom RPC: {os.getenv('RPC_URL')}")

# Serve files from current directory
server = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
server.serve_forever()
