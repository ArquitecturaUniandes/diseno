import os
from flask import Flask
from redis import Redis
from rq import Queue
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY', "secret-jwt")

jwt = JWTManager(app)

# db 1 cola para reporte financiero
q = Queue(connection=Redis(host='redis', port=6379, db=1))
