import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)
