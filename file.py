

class File:
    def __init__(self, path, option) -> None:
        self.f = None
        self.path = path
        self.createFile(option)

    def createFile(self, option):
        self.f = open(self.path, option)

    def getFile(self):
        return self.f

    def write(self, data: str):
        self.f.write(data)

    def close(self):
        self.f.close()
