import os
import json

from bs4 import BeautifulSoup
import collections
collections.Callable = collections.abc.Callable

from flask import Flask
from flask import request
from flask import redirect, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from oauthlib.oauth2 import WebApplicationClient

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
from models.user import User

from dotenv import load_dotenv

#===================================================================================================

load_dotenv()
redispassword = os.getenv('REDISPASSWORD')
googleclient = os.getenv('GOOGLECLIENT')
googlesecret = os.getenv('GOOGLESECRET')
googlediscovery = ("https://accounts.google.com/.well-known/openid-configuration")

#===================================================================================================

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

client = WebApplicationClient(googleclient)

@login_manager.user_loader
def load_user(email: str):
    return User.get(email)

def get_google_provider_cfg():
    return requests.get(googlediscovery).json()

@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri = request.base_url + "/callback",
        scope = ["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response = request.url,
        redirect_url = request.base_url,
        code = code
    )
    token_response = requests.post(
        token_url,
        headers = headers,
        data = body,
        auth = (googleclient, googlesecret),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    
    user = None
    if not db.user_exists(users_email):
        user = User.create(users_email, None)
    else:
        user = User.get(users_email)
    
    login_user(user)

    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

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
def index(): 
    if current_user.is_authenticated:
        return "authenticated: {}".format(current_user.email)
    else:
        return '<a href="/login">Google Login</a>'
    

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

