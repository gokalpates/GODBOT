from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "Server: Running"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_running():
  th = Thread(target=run)
  th.start()