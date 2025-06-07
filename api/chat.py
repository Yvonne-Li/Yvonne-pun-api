# api/chat.py
from http.server import BaseHTTPRequestHandler
import json
import os

try:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
except ImportError:
    client = None

class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        # CORS preflight response
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.wfile.write(json.dumps({'error': 'No data received'}).encode())
                return

            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            user_message = data.get('message', '').strip()
            if not user_message:
                self.wfile.write(json.dumps({'error': 'Missing or empty "message" field.'}).encode())
                return

            # Check if OpenAI client is available and has API key
            if not client or not client.api_key:
                self.wfile.write(json.dumps({'error': 'OpenAI API not configured'}).encode())
                return

            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an AI assistant with a witty sense of humor and a knack for crafting clever puns and wordplay. "
                            "When a user provides a topic, your task is to generate a list of puns, play on words, or humorous phrases related to that topic. "
                            "The wordplay should be original, creative, and aim to elicit a laugh or a groan from the reader."
                        )
                    },
                    {"role": "user", "content": user_message}
                ],
                max_tokens=200
            )

            result = response.choices[0].message.content.strip()
            self.wfile.write(json.dumps({'response': result}).encode())

        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Invalid JSON format'}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': f'Server error: {str(e)}'}).encode())