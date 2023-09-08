from flask import Flask, request, redirect, render_template
from threading import Thread
from flask_socketio import SocketIO, emit, join_room, leave_room
import secrets
import time
import random
from flask_cors import CORS
from utils import toast, get_ip, resource_path
from engineio.async_drivers import threading
import pyautogui
import sys
import os

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
else:
    app = Flask(__name__)

app.config['CORS_ORIGINS'] = '*'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
CORS(app)
codes = []
frontend_client = "giste-client.pop-plays.live" # http://192.168.31.134:3000

import logging
logging.getLogger('werkzeug').setLevel(logging.ERROR)
logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)

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
               return toast('Client Connected', "A new client has connected to your computer.")
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
   
@app.route('/host')
def host():
   return render_template("host.html")

@app.route('/connect')
def connect():
   return render_template("connect.html")


@app.route('/dashboard')
def dashboard():
   return render_template("dashboard.html")

@socketio.on("connect")
def connected():
   print("socket connected!")

def run(debug=False):
  print('Starting GisteDesktop. Do NOT CLOSE THIS TERMINAL AT ANY POINT.')
  socketio.run(app, host='0.0.0.0', port=app.config['PORT'], debug=debug)

def start_server(port, ip):
   app.config['PORT'] = port
   app.config['IP'] = ip

   t = Thread(target=run)
   t.start()

if __name__ == "__main__":
   app.config['PORT'] = 12436
   app.config['IP'] = get_ip()
   run(True)