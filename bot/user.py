import json
from course import Course

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.courses = []
        self.balance = 0
    
    def add_course(self, course):
        self.courses.append(course)
    
    def remove_course(self, course):
        self.courses.remove(course)

    def get_courses(self):
        return self.courses
    
    def get_balance(self):
        return self.balance

    def set_balance(self, balance):
        self.balance = balance
    
    def __str__(self):
        return f"{self.username}"

    def __repr__(self):
        return self.__str__()


