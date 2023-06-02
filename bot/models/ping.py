class Ping:
    def __init__(self, uri, headers, course):
        self.uri = uri
        self.headers = headers
        self.course = course

    def __str__(self):
        return f"{self.course}"

    def __repr__(self):
        return self.__str__()