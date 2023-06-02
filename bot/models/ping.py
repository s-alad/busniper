class Ping:
    def __init__(self, uri, headers):
        self.uri = uri
        self.headers = headers

    def __str__(self):
        return f"uri: {self.uri}, headers: {self.headers}"

    def __repr__(self):
        return self.__str__()