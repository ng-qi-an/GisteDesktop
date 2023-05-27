from flask import Flask, request
from threading import Thread
import pyautogui
import secrets
import time
import json
from utils import encode_base64
app = Flask('')

codes = []

@app.route('/')
def index():
    return {'status': 'OK', "version": "0.1.0-alpha"}

@app.route('/connect')
def connect():
   payload = {
      'code': secrets.token_urlsafe(16),
      'expire': round(time.time()) + 300,
      'port': app.config['PORT'],
      'ip': app.config['IP']
   }
   codes.append(payload)
   print(json.dumps(payload))
   return f'''
   <h1>Connect to Giste</h1>
   <p>The connectoon process is relatively easy. All you need to to is scan the QR code below with the Giste mobile app or the Giste mobile website. Once connected, feel free to close this tab.</p>
   <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={encode_base64(json.dumps(payload))}"/>
   <p style="color: red;">The qr code will expire in 5 minutes! Retry connection process if it fails or expires.</p>
   '''

def run():
  app.run(host='0.0.0.0', port=app.config['PORT'])

def start_server(port, ip):
   app.config['PORT'] = port
   app.config['IP'] = ip

   t = Thread(target=run)
   t.start()