import os
import shutil
import urllib.request as ur
import requests as rq
#import imghdr
from bs4 import BeautifulSoup as bs
import logging

# log
logging.basicConfig(
  filename=os.path.abspath('.')+'/log',
  format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
  datefmt='%H:%M:%S',
  level=logging.DEBUG)
def lg(msg=""):
  logging.debug(msg)
  print(msg)
  
lg("Scraper started")

# create destination folder for download
pics_dir = os.path.abspath('.') + '/pics/'
if not os.path.exists(pics_dir):
  os.makedirs(pics_dir)

uids = input("Input targer usernames separated by space:\n").split()
max_count = int(input("Input max number of downloads for each user:\n"))
print()

lg(("Target usernames = {}\n"
    "Max downloads = {}").format(
uids, max_count))
lg()

# iterate through each target user
for u in uids:
  lg("Now downloading from user: {}".format(u))
  
  # create download folder
  user_dir = pics_dir + u + '/'
  if not os.path.exists(user_dir):
    os.makedirs(user_dir)
  
  # iterate through gallery pages
  count = 0
  pg = 0
  while True:
    gallery_url = 'https://twicsy.com/u/' + u + '/skip/' + str(pg)
    gallery_soup = bs(rq.get(gallery_url).content)
    
    item_container = gallery_soup \
    .find_all(class_='container inner_page')[0]
    
    if "No pics found!" in str(item_container):
      lg("Reached end of gallery of user: " + u)
      lg()
      break

    item_urls = item_container \
    .find_all(class_='image_link trackerClass popper')

    item_urls = ['https://twicsy.com'+str(i).split('href="')[1].split('"')[0] \
                 for i in item_urls]

    # visit item page
    for item in item_urls:
      count += 1
      
      # max count threshold check
      if count > max_count:
        lg("Reached max count!")
        lg()
        break
      
      lg('#' + str(count) + ':')
      
      item_meta = bs(ur.urlopen(item).read()) \
      .find_all(id='outbound.main_pic')

      if len(item_meta) < 1:
        lg("[X] Not a picture! ({})".format(item))
        continue

      item_meta = str(item_meta[0])

      if 'pic.twitter.com' in item_meta:
        image_url = item_meta.split('src="')[1].split('"')[0]
        file_name = image_url.split('/')[-1].split(':')[0]

      elif 'twitpic.com' in item_meta:
        image_url = item_meta.split('href="')[1].split('"')[0]
        image_meta = str(bs(rq.get(image_url).content))
        image_url = image_meta.split('twitter:image" value="')
        
        if not len(image_meta):
          lg("[X] Dead source link! ({})".format(item))
          continue

        image_url = image_url[1].split('"')[0]
        image_url = image_url.replace('&amp;', '&')
        file_name = image_url.split('/')[-1].split('?')[0]

      else:
        lg("[X] Unknown source site! ({})".format(item))
        continue

      try:
        ur.urlretrieve(image_url, user_dir + file_name)
        lg("[O] Successful!")

      except Exception as e:
        lg("[X] Error: {} ({})".format(e, item))
        continue
    
    if count > max_count:
      break
    
    pg += 80

lg("Completed")
