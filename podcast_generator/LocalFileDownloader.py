from .PodcastDownloader import *

### LocalFileDownloader takes a list of local
###   files, and "downloads" them
class LocalFileDownloader(PodcastDownloader):
    def __init__(self, *files):
        PodcastDownloader.__init__(self)
        self.files = []
        for infile in files:
            if type(infile) is list:
                for infile2 in infile:
                    self.addFile(infile2)
            else:
                self.addFile(infile)

    ### addFile adds a local file
    def addFile(self, infile):
        self.files.append(infile)

    ### getFiles will convert and
    ###   make available all files from
    ###  self.files
    def getFiles(self):
        count=0
        for infile in self.files:
            if(self.maxCount is not None and count >= self.maxCount):
                return count
            if self.db.alreadyDownloadedUrl(infile) == False and self.extensionMatch(infile):
                self.db.addDownloadedUrl(infile)
                self.makeFileToPodcast(infile)
                count += 1
        return count
