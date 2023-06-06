import redis
from redis.commands.json.path import Path

import os
import dotenv
import time

from models.ping import Ping
from models.section import Section
from models.course import Course

class Database:

    dotenv.load_dotenv()
    redispassword = os.getenv('REDISPASSWORD') #os.getenv('RAILWAYREDIS') 
    red = redis.Redis(
        host='redis-18876.c232.us-east-1-2.ec2.cloud.redislabs.com',
        port=18876,
        password=redispassword
    ) 

    def __init__(self):
        pass

    def clear_pings(self):
        self.red.json().clear("Pings")

    def get_pings(self):
        return self.red.json().get("Pings")

    def add_ping(self, ping: Ping):
        return self.red.json().arrappend("Pings", "$", ping.__dict__())
    
    def remove_ping(self, ping: Ping):
        return self.red.json().arrpop("Pings", ".", self.red.json().arrindex("Pings", ".",ping.__dict__()))
    
    def add_pings(self, pings: list[Ping]):
        for ping in pings: self.add_ping(ping)
    
    def get_all_course_names(self):
        return list(self.red.json().get("Courses").keys())
    
    def get_all_courses(self):
        return self.red.json().get("Courses")
        
    def get_course(self, course: Course):
        return self.red.json().get("Courses", Path(str(course)), no_escape=True)

    def add_course(self, course: Course):
        return self.red.json().set("Courses", Path(str(course)), {"subscribers" : []})
    
    def remove_course(self, course: Course):
        return self.red.json().delete("Courses", Path(str(course)))
    
    def check_course_exists(self, course: Course):
        return str(course) in self.get_all_course_names()

    def add_subscriber(self, course: Course, email: str):
        return self.red.json().arrappend("Courses", Path(str(course)+".subscribers"), email)
    
    def get_users(self):
        return self.red.json().get("Users")
    
    def get_users_emails(self):
        return list(self.red.json().get("Users").keys())
    
    def get_user(self, email: str):
        return self.red.json().get("Users", email, no_escape=True)
    
    def user_exists(self, email: str):
        return email in self.get_users_emails()
    
    def create_user(self, email: str, number: str):
        u = {
            "active-courses" : [],
            "inactive-courses" : [],
            "number" : number,
            "credits" : 0,
            "email" : email,
        }
        return self.red.json().set("Users", '["{}"]'.format(email), u)
    
    def add_credits(self, email: str, credits: int):
        return self.red.json().numincrby("Users", '["{}"]["{}"]'.format(email, "credits"), credits)
    
    def remove_credits(self, email: str, credits: int):
        return self.add_credits(email, -credits)
    
    def remove_active_course(self, email: str, course: Course):
        index = self.red.json().arrindex("Users", '["{}"]["{}"]'.format(email, "active-courses"), str(course))
        return self.red.json().arrpop("Users", '["{}"]["{}"]'.format(email, "active-courses"), index)
        
    def add_inactive_course(self, email: str, course: Course):
        return self.red.json().arrappend("Users", '["{}"]["{}"]'.format(email, "inactive-courses"), str(course))
    
    def add_active_course(self, email: str, course: Course):
        return self.red.json().arrappend("Users", '["{}"]["{}"]'.format(email, "active-courses"), str(course))

if __name__ == "__main__":
    db = Database()
   # print(db.clear_pings())
    #watchlist = [Course.unwrap(course) for course in db.get_all_course_names()]
    #print(watchlist)
    #for c in watchlist:
    #    print(c.college, c.dept, c.course, c.section)

    #db.remove_ping(Ping("https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1?ModuleName=reg%2Fadd%2Fbrowse_schedule.pl&SearchOptionDesc=Class+Number&SearchOptionCd=S&ViewSem=Fall+2023&KeySem=20243&AddPlannerInd=&College=CAS&Dept=cs&Course=411&Section=A1", Course("CAS", "CS", "411", "A1")))
    #print(db.get_course(Course("CAS", "CS", "237", "A1")))
    #print(db.add_inactive_course("xyz@gmail.com", Course("CAS", "CS", "237", "A1")))

    #print(db.check_course_exists(Course("CAS", "CS", "411", "A1")))

    #print(db.create_user("saad7@bu.edu", "1234567890"))
    #print(db.add_credits("saad7@bu.edu", 1))
    