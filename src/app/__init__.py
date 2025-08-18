from flask import Flask, request, jsonify
from service.messageService import MessageService
from kafka import KafkaProducer
import json

messageService = MessageService()

# Kafka Producer setup
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/v1/ds/message/', methods=['POST'])
def handle_message():
    message = request.json.get('message')
    result = messageService.processMessage(message)

    # Always prepare a dict to send to Kafka + return to client
    if isinstance(result, dict):
        response = result
    elif isinstance(result, str):
        response = {"response": result}
    else:
        response = {"response": str(result)}

    # Send dict directly (KafkaProducer will serialize it)
    producer.send('expense_service', response)

    # Return proper HTTP response
    return jsonify(response), 200


@app.route('/', methods=['GET'])
def handle_get():
    return "Hello World", 200


if __name__ == '__main__':
    # 0.0.0.0 → accessible from outside, port 8000
    app.run(host="0.0.0.0", port=8000, debug=True)