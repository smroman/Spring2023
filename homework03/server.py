import time

from flask import Flask, request, abort
from datetime import datetime
app = Flask(__name__)
db = []

@app.route("/")
def hello():
    return "Hello, World!"

def users():
    users = set()
    for message in db:
        users.add(message["name"])
    return list(users)

@app.route("/status")
def status():
    return {
        "number of users": len(users()),
        "list of users": users(),
        "number of messages": len(db),
        "status": True,
        "big brother mode": db,
        "time": datetime.now().astimezone().strftime("%H:%M:%S %d/%m/%Y")
    }

@app.route("/send", methods=["POST"])
def send_message():
    data = request.json

    if not isinstance(data, dict):
        return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)

    name = data["name"]
    text = data["text"]

    if not isinstance(name, str) or \
            not isinstance(text, str) or \
            name == '' or text == '':
        return abort(400)
    message = {
        'time': time.time(),
        'name': name,
        'text': text
    }
    db.append(message)
    return {"ok": True}

@app.route("/messages")
def get_messages():
    """messages from db after given timestamp"""
    try:
        after = float(request.args['after'])
    except:
        return abort(400)

    result = []
    for message in db:
        if message['time'] > after:
            result.append(message)
            if len(result) >= 100:
                break

    return {"messages": result}

app.run()