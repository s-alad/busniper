class Course:
    college = None
    dept = None
    course = None
    section = None

    def __init__(self, college: str, dept: str, course: str, section=None):
        self.college = college
        self.dept = dept
        self.course = course
        self.section = section if section else None

    def __str__(self):
        return f"{self.college} {self.dept} {self.course} {self.section}"
    
    def __repr__(self):
        return self.__str__()