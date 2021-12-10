from flask import Flask, jsonify, request
from threading import Thread

app = Flask('')

global status
status = True

@app.route('/')
def home():
    return jsonify({"status":status})


def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()