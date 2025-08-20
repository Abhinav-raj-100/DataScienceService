import sys
import importlib

# Force reload kafka-python instead of langchain's kafka.py
if "kafka" in sys.modules:
    del sys.modules["kafka"]

kafka = importlib.import_module("kafka")
from kafka import KafkaProducer
from flask import Flask, request, jsonify
from .service.messageService import MessageService
import json
import os

messageService = MessageService()

# Load env variables with defaults
kafka_host = os.getenv('KAFKA_HOST', 'localhost')
kafka_port = os.getenv('KAFKA_PORT', '9092')
kafka_bootstrap_servers = f"{kafka_host}:{kafka_port}"

print("Kafka server is " + kafka_bootstrap_servers)
print("\n")


# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[kafka_bootstrap_servers],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/v1/ds/message', methods=['POST'])
def handle_message():
    message = request.json.get('message')
    result = messageService.process_message(message)

    # Convert Pydantic model → dict for Kafka + jsonify
    serialized_result = result.dict() # dict

    # Send dict to Kafka (your producer serializer already handles JSON encoding)
    producer.send('expense_service', serialized_result)

    # Send JSON response back to client
    return jsonify(serialized_result)



@app.route('/', methods=['GET'])
def handle_get():
    return "Hello World", 200


if __name__ == '__main__':
    # 0.0.0.0 → accessible from outside, port 8010
    app.run(host="0.0.0.0", port=8010, debug=True)