import os
from bs4 import BeautifulSoup
import collections

collections.Callable = collections.abc.Callable

from flask import Flask
from flask import request

from apscheduler.schedulers.background import BackgroundScheduler

import time
import requests
import atexit
import redis

from bot import Sniper
from models.ping import Ping
from models.section import Section
from models.course import Course
from db import Database

from dotenv import load_dotenv

#===================================================================================================

load_dotenv()
redispassword = os.getenv('REDISPASSWORD')

#===================================================================================================

app = Flask(__name__)

def recur():
    pings = db.get_pings()
    print("current queue =====================")
    print(*pings, sep = "\n")
    print("-----------------------------------")
    for ping in pings:
        p = Ping(ping["uri"], Course.unwrap(ping["course"]))
        empty = bot.snipe(p)
        if empty:
            db.remove_ping(p)
            print("removed " + str(p))

    print("===================================")

@app.route('/register/<college>/<dept>/<course>/<section>')
def register(college: str, dept: str, course: str, section: str):
    course = Course(college, dept, course, section)
    uri = bot.register(course)

    db.add_ping(Ping(uri, course))

    return "Registered for " + str(course)

@app.route('/')
def index(): return "BUSNIPER"

scheduler = BackgroundScheduler()
scheduler.add_job(func=recur, trigger="interval", seconds=60)

def teardown():
    scheduler.shutdown()
    bot.close()

atexit.register(teardown)

if __name__ == '__main__':
    print("connecting to redis")
    db = Database()
    db.clear_pings()
    
    bot = Sniper()
    bot.login()
    bot.getCookies()

    print("generating pings...")
    watchlist = [Course.unwrap(course) for course in db.get_all_course_names()]
    pings = bot.generator(watchlist)
    db.add_pings(pings)

    print("starting scheduler...")
    scheduler.start()

    app.run(debug=False)

