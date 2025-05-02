#kys

from openai import OpenAI
from openai import OpenAIError
import os
import json
from flask import Flask
import datetime

app = Flask(__name__)

class Taskv2:
    def __init__(self):

        
    @app.route('/', methods = ['POST'])
    def InitTaskContext(self):
        now = datetime.datetime.now()

        self.task = app.json.get('task')
        self.context = app.json.get('context')
        self.date = now.date()
        self.time = now.time()

        
