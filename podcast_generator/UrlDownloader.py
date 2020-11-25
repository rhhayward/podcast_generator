import urllib.request as urllib
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from .PodcastDownloader import *

### UrlDownloader downloads files in
###   <a> tags which have the appropriate
###   extensions, as defined by the
###   addExtension function.
class UrlDownloader(PodcastDownloader):
    def __init__(self, *urls):
        PodcastDownloader.__init__(self)
        self.urls = []
        for url in urls:
            self.addUrl(url)

    ### addUrl is an accessor function
    ###   for the urls that will be
    ###   checked for files to download.
    def addUrl(self, url):
        self.urls.append(url)

    ### getFiles is the function that
    ###   will be called to actually
    ###   do the downloading.  It will
    ###   only download as many files
    ###   as self.maxCount allows,
    ###   and return the number of
    ###   files it has downloaded.
    def getFiles(self):
        count=0
        for url in self.urls:
            file = urllib.urlopen(url)
            xmldata = file.read()
            file.close()

            soup = BeautifulSoup(xmldata)
            for link in soup.find_all('a'):
                if(self.maxCount is not None and count >= self.maxCount):
                    return count
                try:
                    link['href'] = urljoin(url, link['href'])
                    if self.db.alreadyDownloadedUrl(link['href']) == False and self.extensionMatch(link['href']):
                        outfn = self.getFilenameFromPath(link['href'])
                        (filename, headers) = urllib.urlretrieve( link['href'], outfn )
                        self.db.addDownloadedUrl(link['href'])
                        self.makeFileToPodcast(filename)
                        count += 1
                except:
                    pass
        return count
