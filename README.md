podcast_downloader provides a set of classes for creating a podcast.

### Ubuntu build and install steps

Install dependencies

```
apt install git python3 python3-setuptools python3-pip python-wheel-common ffmpeg
```

Clone the repo, enter the directory

```
git clone https://github.com/rhhayward/podcast_generator.git
cd podcast_generator
```

Build
```
python3 setup.py sdist bdist_wheel
```

Install

```
cd ..
python3 -m pip install podcast_generator/dist/*.whl
```


### Example

```
#!/usr/bin/env python3

from podcast_generator import *

### Specify database to use.  A new one
###    will be created if it does not exist.
db = PodcastDb("./podcastdb.sqlite")

### PodcastCreator collects downloaders,
###    sets up the location for the files
###    to be downloaded to, 
podcast = PodcastCreator()
podcast.useDb(db)
podcast.setDestFolder("/opt/")
podcast.setMaxCount(1)
podcast.setOutputXmlFile("/opt/rss.xml")
podcast.setTitle("example-podcast")
podcast.setLink("http://exampledomain/rss.xml")
podcast.setEnclosureBaseUrl("http://exampledomain/")

### Create a downloader
downloader = UrlDownloader("https://ia801301.us.archive.org/32/items/VideoTestFiles/")
downloader.addExtension("mp4")
podcast.addDownloader(downloader)

### Execute the download
podcast.getFiles()

### Delete files older than...
podcast.cleanupFiles(3)

### Having downloaded the files,
###   write the rss
podcast.writeOutputFile()
```
