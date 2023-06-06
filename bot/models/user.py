import json
from course import Course

class User:
    def __init__(self, email: str, number: str | None) -> None:
        self.email = email
        self.active_courses = []
        self.inactive_courses = []
        self.number = number
        self.credits = 0


