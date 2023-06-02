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
        snipe(ping.uri, ping.headers)
        print("=====================================")

def snipe(uri, head):
        r = requests.get(uri, headers=head)
        print(r.status_code)
        soup = BeautifulSoup(r.content, 'html5lib')
        form = soup.find('form', attrs = {'name': 'SelectForm'})
        table = form.find('table')
        trs = table.find_all('tr')[3:]

        for tr in trs:
            try:
                tds = tr.find_all('td')
                mark = tds[0].text

                section = Section(
                    marktoadd=mark, 
                    classname=tds[2].text, 
                    titleinstructor=tds[3].text, 
                    openseats=tds[5].text, 
                    credithours=tds[6].text, 
                    classtype=tds[7].text, 
                    building=tds[8].text, 
                    room=tds[9].text, 
                    day=tds[10].text, 
                    start=tds[11].text, 
                    stop=tds[12].text, 
                    notes=tds[13].text)
                
                print(section, ">" ,section.can_add())
            except:
                print("error parsing section")
                continue


@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    uri = data['uri']
    headers = data['headers']
    course: Course = data['course']
    queue.append(Ping(uri, headers, course))
    return "OK"

@app.route('/register/<college>/<dept>/<course>/<section>')
def register(college: str, dept: str, course: str, section: str):
    if section == "": section = None
    course = Course(college, dept, course, section)
    bot.register(course)
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

