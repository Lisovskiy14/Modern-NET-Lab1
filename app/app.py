import os
import socket
from flask import Flask
import redis

app = Flask(__name__)

try:
    r = redis.Redis(host='db', port=6379, db=0, decode_responses=True)
except Exception as e:
    r = None

@app.route('/')
def index():
    if r is None:
         return "Error: There is no connection to DB.\n", 500
    try:
        visits = r.incr('counter')
        hostname = socket.gethostname()
        return f"Hello! You visited this page {visits} times. (Processed by container: {hostname})\n"
    except redis.RedisError as e:
        return f"Redis Error: {e}\n", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
