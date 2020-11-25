class Podcast:
    def __init__(self, fileName=None, date=None):
        self.fileName = fileName
        self.date = date

    def getFileName(self):
        return self.fileName

    def getDate(self):
        return self.date
