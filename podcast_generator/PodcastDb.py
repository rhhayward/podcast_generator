import datetime
import sqlite3
from os.path import basename
from .Podcast import *

### PodcastDb is the class that
###   remembers urls downloaded
###   and files that are available
###   for the rss.
class PodcastDb:
    ### connect to the database and create
    ###   the tables, unless they already exist.
    def __init__(self, databaseFile):
        conn = sqlite3.connect(databaseFile)
        self.c = conn.cursor()
        self.db = conn
        self.c.execute('''CREATE TABLE IF NOT EXISTS downloaded_urls (url text)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS available_files (filename text, pubDate text, dlDate DATETIME)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS additional_fields (filename text, fieldName, fieldValue)''')

    ### insertPodcast stores podcast to database
    ###   for the rss file downloads
    def insertPodcast(self, podcast, date=None):
        if date is None:
            date = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
        self.c.execute( "INSERT INTO available_files VALUES (?,?,datetime('now'))", \
            (basename(podcast.getFileName()),date,) )
        for field in podcast.getAdditionalFields():
            self.c.execute( "INSERT INTO additional_fields VALUES (?,?,?)", \
            (basename(podcast.getFileName()), field['fieldName'], field['fieldValue'],) )

        self.db.commit()

    ### addDownloadedUrl marks a url as
    ###   having been processed, and doesn't
    ###   need to be processed again.
    def addDownloadedUrl(self,url):
        self.c.execute( "INSERT INTO downloaded_urls VALUES (?)", (url,))
        self.db.commit()

    ### alreadyDownloadedUrl checks database
    ###   connect (c) for a db entry of url.
    ###   Returns true if found, false otherwise
    def alreadyDownloadedUrl(self, url):
        self.c.execute(" SELECT 1 FROM downloaded_urls WHERE url=? ", (url,))
        if self.c.fetchone():
            return True
        else:
            return False

    ### getPodcastsFromDb returns a list of the
    ###   Podcasts available for rss downloading.
    def getPodcastsFromDb(self):
        self.c.execute(" SELECT filename, pubDate FROM available_files ORDER BY dlDate DESC")
        dbFiles = self.c.fetchall()
        podcasts = []
        for [dbFile, pubDate] in dbFiles:
            self.c.execute(" SELECT fieldName, fieldValue FROM additional_fields WHERE filename=?", (dbFile,))
            dbFields = self.c.fetchall()
            fields = []
            for [fieldName, fieldValue] in dbFields:
                fields.append({"fieldName": fieldName, "fieldValue": fieldValue})
            podcasts.append(Podcast(fileName=dbFile, date=pubDate, additionalFields=fields))
        return podcasts

    ### cleanupFiles takes a number of days before
    ###    today to remove files from the database
    ###    Returns list of files removed.
    def cleanupFiles(self, count):
        try:
            int(count)
        except:
            return "input not an integer"

        ### Fix and prepare count:  always negative, always
        ###   '-N day'
        if count>0:
            count *= -1
        count = str(count)+" day"

        self.c.execute(" SELECT filename FROM available_files WHERE dlDate <= date('now',?) ", (count,))
        dbFiles = self.c.fetchall()
        files = []
        for [dbFile] in dbFiles:
            files.append(dbFile)

        o = self.c.execute(" DELETE FROM available_files WHERE dlDate <= date('now',?) ", (count,))
        for [dbFile] in dbFiles:
            o = self.c.execute(" DELETE FROM additional_fields WHERE filename=?", (dbFile,))
        self.db.commit()

        return files
