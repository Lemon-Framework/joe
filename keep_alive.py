from flask import Flask, jsonify, request
from threading import Thread
import hmac
import hashlib
import os
import asyncio

app = Flask('')

@app.get('/')
def home():
    return jsonify({"status":True})

@app.post('/deploy')
def deploy():
	response = jsonify({
		'message': 'Unauthorized',
		'code': 401
	})
	response.status_code = 401
	if not request.is_json:
		return response
	if 'TOKEN' not in request.json.keys():
		return response 

	if request.json['TOKEN'] != os.getenv('DEPLOY_TOKEN'):
		return response

	os.system(
'''git fetch --prune origin
git reset --hard HEAD
busybox reboot
'''
	)

	print("[LOG] Deployded succesfuly")
	
	return jsonify({
		'message': 'OK',
		'code': 200
	})
	

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
	t = Thread(target=run)
	t.start()