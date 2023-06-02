from bs4 import BeautifulSoup
import collections
collections.Callable = collections.abc.Callable

from flask import Flask
from flask import request

from apscheduler.schedulers.background import BackgroundScheduler

import time
import requests
import atexit

from bot import Sniper
from models.ping import Ping
from models.section import Section
from models.course import Course

#===================================================================================================

app = Flask(__name__)

queue = []

def recur():
    print("current queue", queue)
    for ping in queue:
        bot.snipe(ping.uri, ping.course)
    print("-----------------------------------")

#@app.route('/add', methods=['POST'])
def add(uri, course):
    #data = request.get_json()
    #uri = data['uri']
    #headers = data['headers']
    #course: Course = data['course']

    queue.append(Ping(uri, course))
    return "OK"

@app.route('/register/<college>/<dept>/<course>/<section>')
def register(college: str, dept: str, course: str, section: str):
    course = Course(college, dept, course, section if section != "" else None)
    uri = bot.register(course)

    add(uri, course)

    return "Registered for " + str(course)

@app.route('/')
def index(): return "BUSNIPER"

scheduler = BackgroundScheduler()
scheduler.add_job(func=recur, trigger="interval", seconds=15)

def teardown():
    scheduler.shutdown()
    bot.close()

atexit.register(teardown)

if __name__ == '__main__':
    scheduler.start()
    bot = Sniper()
    bot.login()
    bot.getCookies()
    app.run(debug=False)

