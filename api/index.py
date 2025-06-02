from http.server import BaseHTTPRequestHandler
import json
import random

# Simple pun database for free deployment
PUN_DATABASE = {
    'programming': [
        "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
        "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings. 💔",
        "Why do Java developers wear glasses? Because they don't C#! 👓",
        "How do you comfort a JavaScript bug? You console it! 🖥️",
        "Why did the programmer quit his job? He didn't get arrays! 📊",
        "What's a programmer's favorite hangout place? Foo Bar! 🍺",
        "Why do programmers hate nature? It has too many bugs! 🌿",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡"
    ],
    'data': [
        "I'm really Excel-lent at data analysis! 📊",
        "Data scientists have the best tables! 📋", 
        "I'm having a SQL good time with databases! 💾",
        "This dataset is absolutely data-licious! 🍰",
        "My relationship status: In a relation-ship with my database! 💕",
        "I'm mean about averages! 📈",
        "Statistics don't lie, but they might exaggerate! 📉"
    ],
    'coffee': [
        "Thanks a latte for being brew-tiful! ☕",
        "You're brew-tiful just the way you are! ✨",
        "Life happens, coffee helps! ☕",
        "Espresso yourself! 💪",
        "I love you a latte! ❤️",
        "Why did the coffee file a police report? It got mugged! 🚔"
    ],
    'food': [
        "What do you call cheese that isn't yours? Nacho cheese! 🧀",
        "Why don't eggs tell jokes? They'd crack each other up! 🥚",
        "What do you call a fake noodle? An impasta! 🍝",
        "Why did the banana go to the doctor? It wasn't peeling well! 🍌",
        "Why did the cookie go to the doctor? Because it felt crumbly! 🍪"
    ],
    'animals': [
        "What do you call a sleeping bull? A bulldozer! 🐂",
        "Why don't elephants use computers? They're afraid of the mouse! 🐘",
        "What do you call a bear with no teeth? A gummy bear! 🐻",
        "Why don't oysters donate? Because they are shellfish! 🦪",
        "What do you call a fish wearing a crown? A king fish! 👑",
        "Why don't cats play poker in the jungle? Too many cheetahs! 🐱"
    ],
    'toronto': [
        "Toronto is CN-credible! 🏙️",
        "I'm having a Tor-onto-p time in this city! 🎉",
        "This city really knows how to maple me happy! 🍁",
        "Toronto: where the 6ix meets perfection! ✨",
        "I'm totally hoser over heels for this city! ❤️"
    ],
    'general': [
        "Why don't scientists trust atoms? Because they make up everything! ⚛️",
        "What do you call a fake stone? A shamrock! 🍀",
        "Why did the math book look so sad? Because it had too many problems! 📚",
        "I told my wife she was drawing her eyebrows too high. She looked surprised! 😮",
        "What do you call a parade of rabbits hopping backwards? A receding hare-line! 🐰",
        "Why did the scarecrow win an award? He was outstanding in his field! 🌾"
    ]
}

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
            
            message = data['message'].lower()
            
            # Simple keyword matching
            category = 'general'
            if any(word in message for word in ['programming', 'code', 'developer', 'computer', 'software', 'bug', 'javascript', 'python', 'java', 'coding']):
                category = 'programming'
            elif any(word in message for word in ['data', 'analytics', 'database', 'sql', 'excel', 'statistics', 'analysis']):
                category = 'data'
            elif any(word in message for word in ['food', 'eat', 'cook', 'restaurant', 'hungry', 'cheese', 'egg', 'cookie']):
                category = 'food'
            elif any(word in message for word in ['coffee', 'latte', 'espresso', 'brew']):
                category = 'coffee'
            elif any(word in message for word in ['animal', 'dog', 'cat', 'pet', 'zoo', 'bear', 'fish', 'elephant']):
                category = 'animals'
            elif any(word in message for word in ['toronto', 'canada', 'canadian', '6ix']):
                category = 'toronto'
            
            # Get random puns from the category
            available_puns = PUN_DATABASE[category]
            num_puns = min(5, len(available_puns))
            selected_puns = random.sample(available_puns, num_puns)
            
            response_text = "\n\n".join(selected_puns)
            
            self.end_headers()
            self.wfile.write(json.dumps({'response': response_text}).encode())
            
        except Exception as e:
            self.end_headers()
            self.wfile.write(json.dumps({'error': f'Something went wrong: {str(e)}'}).encode())
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()