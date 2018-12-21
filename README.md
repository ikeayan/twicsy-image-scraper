# Twicsy Image Scraper

## Description

Image scraper for Twicsy.com

Capable of downloading image files that are hosted on pic.twitter.com or twitpic.com, from multiple users with a custom max download threshold.

Does not support downloading images hosted on other sites and other contents including animated videos.

## Usage

### Requirements

* python
  * requests
  * bs4

### Run
Run the python script

```
$ python ./scraper.py
```

And follow the instructions displayed on the console,

which requires input of target user names (separated by space) and a maximum number of downloads.

User names should be the unique Twitter handles that starts with a '@', enter without the '@'.

### Retrieve Files

The script will generate a __pics__ sub-directory under the directory where the script is placed.

Within the __pics__ sub-directory there will be sub-directories for each user labeled with their respective handle, in which stores all the downloads for that user.

The downloaded files will have the same filenames as how they are hosted.

The directories and files above will not be deleted by the script, downloading a file with an existing filename will simply overwrite the older file.