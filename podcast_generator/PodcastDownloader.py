import re
import os
import shutil
import subprocess
from .Podcast import Podcast

### PodcastDownloader is the
###   foundation class for all other
###   downloaders.
class PodcastDownloader:
    def __init__(self):
        self.destFolder = None
        self.maxCount = None
        self.db = None
        self.extensions = []
        self.filters = []
        self.excludeFilters = []
        self.outputFormat = ".mp4"
        self.doConvert = True

    def getOutputFormat(self):
        return self.outputFormat

    def setDoConvert(self, convert):
        self.doConvert = convert

    def setOutputFormat(self, inFormat):
        self.outputFormat = inFormat

    ### slugify takes an arbitrary string and
    ###   converts it to be usable as a filename.
    def slugify(self, value):
        """
        Normalizes string, converts to lowercase, removes non-alpha characters,
        and converts spaces to hyphens.
        """
        import unicodedata
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        value = re.sub('[^\w\s-]', '', str(value)).strip().lower()
        value = re.sub('[-\s]+', '-', value)
        value = re.sub('^-+', '', value)
        return value


    ### addExtension takes the file extension, without
    ###   dot prefix.  Used to build the file name
    ###   retular expressions for matching files.
    def addExtension(self, extension):
        self.extensions.append(extension)

    ### addFilter takes a regex filter to limit
    ###   items to be  downloaded.
    def addFilter(self, filter):
        self.filters.append(filter)

    ### addExcludeFilter takes a regex filter to exclude
    ###   items to be downloaded.
    def addExcludeFilter(self, filter):
        self.excludeFilters.append(filter)

    ### filterMatch checks the name parameter vs
    ###   all filters.
    def filterMatch(self, name):
        ### If we have exclude filters, check them first
        ###    to see if any cause us to reject
        if len(self.excludeFilters) > 0:
            for filter in self.excludeFilters:
                if( re.search(filter, name) ):
                    return False

        ### If we have filters, check them.  If any
        ###    match, return true.  Else false
        if len(self.filters) > 0:
            for filter in self.filters:
                if( re.search(filter, str(name)) ):
                    return True
            return False
        ### If we don't have filters, just return True
        return True

    ### extensionMatch takes name as input, and
    ###   compares it to self.extensions[] nd
    ###   function which returns True if the filename
    ###   matches, False otherwise
    def extensionMatch(self, name):
        if re.search(self.buildExtensionRegex(), name):
            return True
        else:
            return False

    ### buildExtensionRegex returns a regex
    def buildExtensionRegex(self):
        if(self.extensions):
            return '\.(' + '|'.join(self.extensions) + ')$'
        else:
            return ''

    ### makeFileToPodcast takes an extant
    ###   file, converts it to an m4v if
    ###   that function can do it, and
    ###   then moves it to the destFolder,
    ###   if it exists.
    def makeFileToPodcast(self, filename, additionalFields=[]):
        convertReturn = self.convertToM4v(filename)

        if(convertReturn):
            convertedFilename=convertReturn
        else:
            convertedFilename=filename

        p = Podcast(fileName=convertedFilename, additionalFields=additionalFields)
        self.db.insertPodcast(p)

        if not self.destFolder is None:
            shutil.copy(convertedFilename,self.destFolder)
            os.remove(convertedFilename)

        try:
            os.remove(filename)
        except:
            pass

    ### getFilenameFromPath takes a path
    ###   (url or unix path) and extracts
    ###   the filename from it.
    def getFilenameFromPath(self, path):
        filename = re.sub('.*/','',path)
        return filename

    ### useDb is an accessor function
    ###   for the podcast database object.
    def useDb(self, db):
        self.db = db

    ### setMaxCount is an accessor
    ###   function for the downloader's
    ###   maximum number of files to
    ###   download.
    def setMaxCount(self, count):
        self.maxCount = count;

    ### setDestFolder is an accessor
    ###   function for the location
    ###   where the downloaded files
    ###   to be moved to.
    def setDestFolder(self, destFolder):
        self.destFolder = destFolder

    ### converToM4v takes as input a
    ###   filename, determines if it's
    ###   convertible to m4v, and does
    ###   it if so.  It returns the
    ###   converted filename if successful,
    ###   else False.
    ### Instructions to get the appropriate
    ###   version of avconv installed in
    ###   Ubuntu:
    ###      from url:  http://www.tomechangosubanana.com/2012/video-conversion-for-iphone-with-avconv/
    ###   apt-get install avconv libavcodec-extra-53 libx264-123 x264  ### note - -53 and -123 were
    ###      replaced by up to date numbers
    def convertToM4v(self, file):
        if self.doConvert is False:
            return False

        if( re.search('\.(mov|avi|mpg|mpeg|mp4|flv|mkv|m4a)$', file) ):
            outputFile = file
            outputFile += self.getOutputFormat()
            if self.getOutputFormat() == ".mp3":
                #stdout = open("/tmp/mencoder.out", "wb")
                #stderr = open("/tmp/mencoder.err", "wb")
                returnCode = subprocess.call([
                    'ffmpeg',
                    '-re',
                    '-i', file,
                    '-threads', '1',
                    outputFile,
                    #'-ovc','frameno',
                    #'-oac','mp3lame','-lameopts','cbr:br=128','-of','rawaudio'
                    ],
                        #stdout=stdout, stderr=stderr
                    )

            else:
                returnCode = subprocess.call([
                    'ffmpeg',
                    '-re',
                    '-i', file,
                    '-threads', '1',
                    #'-vcodec', 'libx264', '-vprofile', 'high',
                    #'-preset', 'slow',
                    #'-b:v', '500k', '-maxrate', '1000k',
                    #'-bufsize', '2000k', '-vf', 'scale=1136:474',
                    #'-acodec', 'libvo_aacenc', '-b:a', '192k',
                    '-strict', '-2',
                    outputFile,
                    ])
            return outputFile
        else:
            return False

    ### Although PodcastDownloader can't
    ###   actually download anything
    ###   itself, it needs a getFiles
    ###   function just in case:
    def getFiles(self):
        return 0
