import json
from models.course import Course
from models.section import Section
from models.ping import Ping
from db import Database

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, email: str, number: str | None, active: list | None, inactive: list | None, credits: int) -> None:
        self.email = email
        self.number = number
        self.active_courses = active if active else []
        self.inactive_courses = inactive if inactive else []
        self.credits = credits if credits else 0

    def __str__(self) -> str:
        return f"{self.email} | {self.number} | {self.active_courses} | {self.inactive_courses} | {self.credits}"
    
    #override get_id() method
    def get_id(self):
        return self.email

    @staticmethod
    def get(email: str):
        db = Database()
        u = db.get_user(email)
        user = User(
            email = u["email"],
            number = u["number"],
            active = u["active-courses"],
            inactive = u["inactive-courses"],
            credits = u["credits"]
        )
        return user
    
    @staticmethod
    def create(email: str, number: str | None):
        db = Database()
        db.create_user(email, number)
        return User.get(email)



