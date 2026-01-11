#!/usr/bin/env python3
import time

from podcast_generator import *
from os import listdir
from os.path import isfile, join

print("starting file_dler")

### Create podcast, connect to db, set output folder
myPodcast = PodcastCreator()
myPodcast.useDb(PodcastDb("/tmp/files.sqlite"))
myPodcast.setDestFolder("/tmp/")

### setup rss fields
myPodcast.setOutputXmlFile("/tmp/file_dler.xml")
myPodcast.setTitle("file_dler example")
myPodcast.setLink("http://example/")
myPodcast.setEnclosureBaseUrl("http://example/")

### list files
path = "/tmp/downloads/"
os.makedirs(path, exist_ok=True)
files = [join(path,f) for f in listdir(path) if isfile(join(path, f))]
files.sort()

### create local file downloader to handle mp3 and m4b files
file_dler = LocalFileDownloader(files)
file_dler.addExtension("mp3")
file_dler.addExtension("m4b")

### add downloader to podcast
myPodcast.addDownloader(file_dler);

## generate podcast
out = myPodcast.getFiles()
myPodcast.writeOutputFile()

print("ending file_dler")
