# api/index.py
from http.server import BaseHTTPRequestHandler
import json
import random
import os

try:
    import openai
    openai.api_key = os.environ.get("OPENAI_API_KEY")
except ImportError:
    openai = None

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

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # CORS
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        topic = data.get('message', '').strip().lower()

        # 1. Try OpenAI first
        if openai and openai.api_key:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an AI assistant with a witty sense of humor and a knack for crafting clever puns and wordplay. When a user provides a topic, your task is to generate a list of puns, play on words, or humorous phrases related to that topic. The wordplay should be original, creative, and aim to elicit a laugh or a groan from the reader."},
                        {"role": "user", "content": f"Tell me puns about {topic}"}
                    ]
                )
                pun = response.choices[0].message['content']
                self.wfile.write(json.dumps({ "response": pun.strip() }).encode())
                return
            except Exception as e:
                print("OpenAI failed, falling back to local puns:", e)

        # 2. Fallback to local pun database
        fallback_key = next((key for key in PUN_DATABASE if key in topic), 'general')
        fallback_puns = PUN_DATABASE.get(fallback_key, PUN_DATABASE['general'])
        puns = random.sample(fallback_puns, k=min(3, len(fallback_puns)))
        self.wfile.write(json.dumps({ "response": "\n".join(puns) }).encode())
        self.wfile.write(json.dumps({ "response": pun }).encode())
