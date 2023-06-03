import redis
from redis.commands.json.path import Path

import os
import dotenv
import time

from models.ping import Ping
from models.section import Section
from models.course import Course

dotenv.load_dotenv()

redispassword = os.getenv('REDISPASSWORD') #os.getenv('RAILWAYREDIS') 
red = redis.Redis(
    host='redis-18876.c232.us-east-1-2.ec2.cloud.redislabs.com',
    port=18876,
    password=redispassword
) 

#generally takes .2s to add and .07s to fetch
def add():
    ...

def get_all_courses():
    c = red.json().get("Courses")
    print(c)

def get_course(course: Course):
    return red.json().get("Courses", Path(str(course)), no_escape=True)

def add_course(course: Course):
    addition = {"subscribers" : []}
    return red.json().set("Courses", Path(str(course)), addition)

def add_subscriber(course: Course, email: str):
    return red.json().arrappend("Courses", Path(str(course)+".subscribers"), email)

""" start = time.time()
print(get_course(Course("CAS", "CS", "237", "A1")))
end = time.time()
print(end - start) """

#print(add_course(Course("CAS", "CS", "112", "A1")))
print(add_subscriber(Course("CAS", "CS", "112", "A1"), "lol@lol.com"))


#print(red.json().get(str(Course("CAS", "CS", "237", "A1"))))