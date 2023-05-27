from flask import Flask, request
from threading import Thread
import pyautogui
import secrets
import time
import json
app = Flask('')

codes = []

@app.route('/')
def index():
    return {'status': 'OK', "version": "0.1.0-alpha"}

@app.route('/connect')
def connect():
   payload = {
      'code': secrets.token_urlsafe(16),
      'expire': round(time.time()) + 300
   }
   codes.append(payload)
   return f'''
   <h1>Connect to Giste</h1>
   <p>The connectoon process is relatively easy. All you need to to is scan the QR code below with the Giste mobile app or the Giste mobile website.</p>
   <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={json.dumps(payload)}"/>
   <p style="color: red;">The qr code will expire in 5 minutes! Retry connection process if it fails or expires.</p>
   '''

def run():
  app.run(host='0.0.0.0', port=app.config['PORT'])

def start_server(port):
    app.config['PORT'] = port
    t = Thread(target=run)
    t.start()