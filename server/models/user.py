import json
from course import Course
from section import Section
from ping import Ping
from db import Database

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, email: str, number: str | None, active: list | None, inactive: list | None, credits: int) -> None:
        self.email = email
        self.number = number
        self.active_courses = active if active else []
        self.inactive_courses = inactive if inactive else []
        self.credits = credits if credits else 0

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



