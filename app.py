from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize OpenAI client using environment variables from .env
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    organization=os.getenv('OPENAI_ORG_ID')
)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if 'message' not in data:
            return jsonify({'error': 'Message field is missing'}), 400

        user_message = data['message']

        # Create response from OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant with a witty sense of humor and a knack for crafting clever puns and wordplay. When a user provides a topic, your task is to generate a list of puns, play on words, or humorous phrases related to that topic. The wordplay should be original, creative, and aim to elicit a laugh or a groan from the reader."},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({'response': response.choices[0].message.content})

    except Exception as e:
        logging.error(f"Error during processing: {str(e)}")
        return jsonify({'error': 'An error occurred during processing. Please try again later.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)