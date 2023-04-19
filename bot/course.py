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
    
class Section:
    marktoadd = None
    classname = None
    titleinstructor = None
    openseats = None
    credits = None
    classtype = None
    building = None
    room = None
    day = None
    start = None
    stop = None
    notes = None

    canadd = False

    def __init__(self, marktoadd, classname, titleinstructor, openseats, credits, classtype, building, room, day, start, stop, notes):
        self.marktoadd = marktoadd
        self.classname = classname
        self.titleinstructor = titleinstructor
        self.openseats = openseats
        self.credits = credits
        self.classtype = classtype
        self.building = building
        self.room = room
        self.day = day
        self.start = start
        self.stop = stop
        self.notes = notes
    
    def __str__(self):
        return f"{self.classname} {self.titleinstructor} {self.classtype} {self.building} {self.room} {self.day} {self.start} {self.stop}"
    
    def __repr__(self):
        return self.__str__()
    
    def can_add(self):
        return self.canadd
    
    def set_can_add(self, canadd):
        self.canadd = canadd
    