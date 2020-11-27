class Podcast:
    def __init__(self, fileName=None, date=None, additionalFields=None):
        self.fileName = fileName
        self.date = date
        self.additionalFields = additionalFields

    def getFileName(self):
        return self.fileName

    def getDate(self):
        return self.date

    def getAdditionalFields(self):
        return self.additionalFields
