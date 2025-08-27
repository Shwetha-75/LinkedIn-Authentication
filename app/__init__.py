from flask import Flask
from app.routes.route import route

def createApp():
    app=Flask(__name__)
    app.register_blueprint(route)
    return app 