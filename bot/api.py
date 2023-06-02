from bs4 import BeautifulSoup
import collections ; collections.Callable = collections.abc.Callable
from flask import Flask
from flask import request
import time
from apscheduler.schedulers.background import BackgroundScheduler
import requests

from course import Course, Section
from bot import Sniper
from models.ping import Ping

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


@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    uri = data['uri']
    headers = data['headers']
    queue.append(Ping(uri, headers))
    return "OK"

@app.route('/')
def index(): return "BUSNIPER"

scheduler = BackgroundScheduler()
scheduler.add_job(func=recur, trigger="interval", seconds=15)

if __name__ == '__main__':
    scheduler.start()
    app.run(debug=True)