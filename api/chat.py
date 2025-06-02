from http.server import BaseHTTPRequestHandler
import json
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'),
    organization=os.environ.get('OPENAI_ORG_ID')
)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Handle CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')
        
        try:
            # Get request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            if 'message' not in data:
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Message field is missing'}).encode())
                return
            
            user_message = data['message']
            
            # Create response from OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an AI assistant with a witty sense of humor and a knack for crafting clever puns and wordplay. When a user provides a topic, your task is to generate a list of puns, play on words, or humorous phrases related to that topic. The wordplay should be original, creative, and aim to elicit a laugh or a groan from the reader."
                    },
                    {"role": "user", "content": user_message}
                ]
            )
            
            self.end_headers()
            self.wfile.write(json.dumps({
                'response': response.choices[0].message.content
            }).encode())
            
        except Exception as e:
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': f'An error occurred: {str(e)}'
            }).encode())
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()