from flask import Flask, jsonify, request
from threading import Thread
import hmac
import hashlib
import os
import asyncio

app = Flask('')

@app.route('/')
def home():
    return jsonify({"status":True})

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
	t = Thread(target=run)
	t.start()