import datetime
from flask import Flask
from redis import Redis
from rq import Queue


app = Flask(__name__)

# db 1 cola para reporte financiero
q = Queue(connection=Redis(host='redis', port=6379, db=1))
