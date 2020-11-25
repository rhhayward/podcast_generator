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
