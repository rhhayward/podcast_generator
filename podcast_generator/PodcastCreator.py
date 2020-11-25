import urllib.request as urllib
from lxml import etree
import os
from os.path import basename
from urllib.parse import urlparse

### PodcastCreator is the class that
###   takes a set of downloaders,
###   sets their settings, takes
###   their downloaded files and
###   makes them into an rss file
###   for use with podcast
###   aggregators.
class PodcastCreator:
    """ takes a list of files, creates an output xml file for use with podcatcher  """

    def __init__(self):
        self.files = []
        self.outputFile = ""
        self.title = ""
        self.link = ""
        self.enclosureBaseUrl =  ""
        self.db = None
        self.destFolder = None
        self.maxCount = None
        self.downloaders = []
        os.chdir("/tmp")

    ### addDownloader takes a PodcastDownloader
    ###   object, sets its dest folder and
    ###   db, and adds it to the list of
    ###   available downloaders.
    def addDownloader(self, Downloader):
        if not self.destFolder is None:
            Downloader.setDestFolder(self.destFolder)
        if not self.db is None:
            Downloader.useDb(self.db)
        self.downloaders.append(Downloader)

    ### getFiles iterates through all
    ###   the available downloaders,
    ###   set their maxCount to our
    ###   maxCount, and decrement our
    ###   maxCount by however many
    ###   the downloader got.
    def getFiles(self):
        downloadedCount=0
        for downloader in self.downloaders:
            if(self.maxCount is not None and downloader.maxCount is None):
                downloader.setMaxCount(self.maxCount)
            count = downloader.getFiles()
            downloadedCount += count
            if(self.maxCount is not None):
                self.maxCount -= count

        return downloadedCount

    ### setMaxCount is an accessor function
    ###   for the maxCount which regulates
    ###   the number of files to download.
    def setMaxCount(self, count):
        self.maxCount = count;

    ### setDestFolder takes a destionation
    ###   folder to move files to after
    ###   they've been downloaded.
    def setDestFolder(self, destFolder):
        self.destFolder = destFolder

    ### useDb is an accessor function
    ###   for the podcast database object.
    def useDb(self, db):
        self.db = db

    ### setLink is used in the rss file for
    ###   the rss link tag.
    def setLink(self, link):
        self.link = link

    ### setEnclosureBaseUrl is where the
    ###   files will be avilable for http
    ###   download.
    def setEnclosureBaseUrl(self, enclosureBaseUrl):
        self.enclosureBaseUrl = enclosureBaseUrl

    ### setOutputXmlFile is the location
    ###   where the rss file will be written.
    def setOutputXmlFile(self, updatedOutputFile):
        self.outputFile = updatedOutputFile

    ### setTitle sets the title of the rss
    ###   file.
    def setTitle(self, title):
        self.title = title

    ### writeOutputFile generates the output
    ###   xml file.
    def writeOutputFile(self):
        self.podcasts = self.db.getPodcastsFromDb()
        fh = open(self.outputFile, "wb")

        channel = etree.Element("channel")
        etree.SubElement(channel, "title").text = self.title
        etree.SubElement(channel, "description").text = self.title
        etree.SubElement(channel, "link").text = self.link
        etree.SubElement(channel, "language").text = "en-us"
        etree.SubElement(channel, "copyright").text = "Copyright 2999"

        for podcast in self.podcasts:
            file = podcast.getFileName()
            pubDate = podcast.getDate()
            item = etree.SubElement(channel, "item")
            etree.SubElement(item, "title").text = file
            etree.SubElement(item, "enclosure").set("url", self.enclosureBaseUrl + urllib.quote(file))
            etree.SubElement(item, "category").text = "Podcasts"
            etree.SubElement(item, "pubDate").text = pubDate

        fh.write(etree.tostring(channel, encoding='UTF-8', xml_declaration=True, pretty_print=True))
        fh.close()

    ### cleanupFiles takes a number of days before
    ###    today to remove files from the fs and db
    ###    Returns count of files removeD
    def cleanupFiles(self, count):
        files = self.db.cleanupFiles(count)
        for file in files:
            try:
                os.unlink(self.destFolder+file)
            except:
                "there was a problem removing file " + self.destFolder+file
