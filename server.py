from flask import Flask, request
from threading import Thread
from flask_socketio import SocketIO, emit, join_room, leave_room
import secrets
import time
import random
from flask_cors import CORS
from utils import toast
import pyautogui
app = Flask('')
app.config['CORS_ORIGINS'] = '*'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
codes = []
frontend_client = "http://192.168.31.134:3000" # http://giste-client.pop-plays.live

def check_code(key):
   for data in codes:
      if data['code'] == key:
         if data.get('expire'):
            if data.get('expire') >= round(time.time()):
               return True
         return True
   return False

@app.route('/')
def index():
    return {'status': 'OK', "version": "0.1.0-alpha"}

@app.route('/shutdown')
def shutdown():
   socketio.stop()

@socketio.on('verifyPin')
def verifyPin(res):
   for data in codes:
      if data['pin'] == res['pin']:
         if data.get('expire'):
            if data['expire'] > round(time.time()):
               del data['expire']
               emit('verifyPin', to=data['code'])
               emit('verifyPin', {'status': 'OK', 'data': data})
               toast('Client Connected', "A new client has connected to your computer.")
            break
         else:
            break
   emit('verifyPin', {'status': 'INVALID'})

@socketio.on('verifyCode')
def verifyCode(res):
   if (check_code(res['code'])):
      emit('verifyCode', {'status': 'OK'})
   else:
      emit('verifyCode', {'status': 'INVALID'})

@socketio.on('evaluate')
def verifyCode(res):
   if (check_code(res['code'])):
      eval(res['data'])
      emit('evaluate', {'status': 'OK'})
   else:
      emit('evaluate', {'status': 'INVALID'})


@socketio.on('createCode')
def createCode(res):
   while True:
      pin = random.randint(1000, 9999)
      counter = 0
      for data in codes:
         if data['pin'] == pin:
            counter += 1
            break
      if counter > 1:
         continue
      else:
         break
   
   payload = {
      'code': secrets.token_urlsafe(16),
      'expire': round(time.time()) + 300,
      'port': app.config['PORT'],
      'ip': app.config['IP'],
      'pin': str(pin)
   }
   codes.append(payload)
   join_room(payload['code'])
   emit('createCode', {'status': 'OK', 'data': {'ip': payload['ip'], 'pin': payload['pin'], 'port': payload['port']}})
   
@app.route('/connect')
def connect():
   return f"""
   <head>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
   </head>
   <style>
      body, html {{
         margin: 0;
         padding: 0;
      }}
   </style>
   <iframe style="height: 100%; width: 100%; border: none;" src='{frontend_client}/connect?port={app.config['PORT']}'/>
   """


@app.route('/dashboard')
def dashboard():
   return f"""
   <head>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
   </head>
   <style>
      body, html {{
         margin: 0;
         padding: 0;
      }}
   </style>
   <iframe style="height: 100%; width: 100%; border: none;" src='{frontend_client}?ip={app.config['IP']}&port={app.config['PORT']}&pin={request.args.get('pin') or ""}'/>
   """

def run():
  print('=== running server ===')
  socketio.run(app, host='0.0.0.0', port=app.config['PORT'])

def start_server(port, ip):
   app.config['PORT'] = port
   app.config['IP'] = ip

   t = Thread(target=run)
   t.start()