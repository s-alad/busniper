class Section:
    marktoadd = None
    classname = None
    titleinstructor = None
    openseats = None
    credithours = None
    classtype = None
    building = None
    room = None
    day = None
    start = None
    stop = None
    notes = None

    def __init__(self, marktoadd, classname, titleinstructor, openseats, credithours, classtype, building, room, day, start, stop, notes):
        self.marktoadd = marktoadd
        self.classname = classname
        self.titleinstructor = titleinstructor
        self.openseats = openseats.strip()
        self.credithours = credithours
        self.classtype = classtype
        self.building = building
        self.room = room
        self.day = day
        self.start = start.strip()
        self.stop = stop.strip()
        self.notes = notes
    
    def __str__(self):
        return f"{self.marktoadd} | {self.classname} | {self.titleinstructor} | {self.openseats} | {self.credithours} | {self.classtype} | {self.building} | {self.room} | {self.day} | {self.start} | {self.stop} | {self.notes}"
    
    def __repr__(self):
        return self.__str__()
    
    def is_section(self, section: str):
        if section == None: return True
        return self.classname.replace(u'\xa0', u' ').split(" ")[2] == section
    
    def can_add(self):
        if str(self.openseats) == "0":
            return False
        if "Full" in str(self.notes).strip() or "Full" == str(self.notes).strip():
            return False
        return True