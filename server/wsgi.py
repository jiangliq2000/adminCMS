#!/usr/bin/env python3
import os
import logging
from logging.config import fileConfig

from app import create_app
import datetime

from flask import redirect, render_template



fileConfig('conf/log-app.conf')
logger = logging.getLogger(__name__)


gunicorn_error_handlers = logging.getLogger('gunicorn.error').handlers



application = create_app(os.getenv('FLASK_CONFIG') or 'default')

application.logger.handlers.extend(gunicorn_error_handlers )

"""
@app.before_request
def before_request():
    print("receive request")
    print(datetime.datetime.now())


@app.after_request
def record_loginUser(response):
    print("after request")
    print(datetime.datetime.now())    
    return response

@app.route('/')
def index():
    return render_template('index.html')
"""


if __name__ == '__main__':
    logger.info("###########################################################")
    logger.info("----------receiver restart --------------")
    logger.info("###########################################################")
    application.run()
