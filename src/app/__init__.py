from flask import Flask, request, jsonify
from service.messageService import MessageService

messageService = MessageService()

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/v1/ds/message/', methods=['POST'])
def handle_message():
    message = request.json.get('message')
    result = messageService.processMessage(message)

    # Ensure we return JSON (not a raw object)
    if isinstance(result, dict):
        return jsonify(result)
    elif isinstance(result, str):
        return jsonify({"response": result})
    else:
        # fallback if it's a custom object, convert to string
        return jsonify({"response": str(result)})

@app.route('/', methods=['GET'])
def handle_get():
    return "Hello World", 200   # ✅ return HTTP response instead of print()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)  # ✅ 0.0.0.0 allows external access too
