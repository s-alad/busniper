class Ping:
    def __init__(self, uri, course):
        self.uri = uri
        #self.headers = headers
        self.course = course

    def __str__(self):
        return f"{self.course}"

    def __repr__(self):
        return self.__str__()
    
    def __dict__(self):
        return {
            "uri": self.uri,
            #"headers": self.headers,
            "course": str(self.course)
        }
    
    def obj(self):
        return {
            "uri": self.uri,
            #"headers": self.headers,
            "course": self.course
        }