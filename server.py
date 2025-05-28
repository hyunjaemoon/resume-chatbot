from flask import Flask, request, jsonify, render_template_string, send_from_directory
from resume_chatbot_agent import ResumeChatbotAgent
import os

app = Flask(__name__, static_folder='ui')
chatbot = ResumeChatbotAgent()

def read_template():
    with open('ui/index.html', 'r') as f:
        return f.read()

@app.route('/')
def home():
    return render_template_string(read_template())

@app.route('/styles/<path:filename>')
def serve_styles(filename):
    return send_from_directory('ui/styles', filename)

@app.route('/scripts/<path:filename>')
def serve_scripts(filename):
    return send_from_directory('ui/scripts', filename)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    data_url = data.get('data_url')
    history = data.get('history', [])

    if not message or not data_url:
        return jsonify({'error': 'Missing message or file'}), 400

    response = chatbot.chat(message, data_url, history)
    return jsonify({'response': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
