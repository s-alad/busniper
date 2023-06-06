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
from mail import Mail
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


def found(p: Ping):
    print("found empty seat for " + str(p))
    subscribers = db.get_course(p.course)["subscribers"]
    #mail.send(p.course, p.uri, subscribers)
    db.remove_ping(p)
    db.remove_course(p.course)
    for email in subscribers:
        db.remove_active_course(email, p.course)
        db.add_inactive_course(email, p.course)

    print("removed " + str(p))

def recur():
    pings = db.get_pings()
    print("current queue =====================")
    print(*pings, sep = "\n")
    print("-----------------------------------")
    for ping in pings:
        p = Ping(ping["uri"], Course.unwrap(ping["course"]))
        empty = bot.snipe(p)
        if empty: found(p)

    print("===================================")

@app.route("/signup", methods=['POST'])
def signup():
    email = request.form["email"]
    number = request.form["number"] if "number" in request.form else None
    if email.split("@")[1] != "bu.edu": 
        return "invalid email"
    if db.user_exists(email): 
        return "please login"
    else:
        db.create_user(email, number)
        return "success"

@app.route('/register/<college>/<dept>/<course>/<section/<email>')
def register(college: str, dept: str, course: str, section: str, email: str):
    course = Course(college, dept, course, section)

    if db.check_course_exists(course):
        db.add_subscriber(course, email)
        db.add_active_course(email, course)
    else:
        db.add_course(course)
        uri = bot.register(course)
        db.add_ping(Ping(uri, course))
        db.add_subscriber(course, email)
        db.add_active_course(email, course)

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

    #mail = Mail()

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

