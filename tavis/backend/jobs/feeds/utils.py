"""
Created by Anthony Velardi on 10/25/18

"""
import requests
import io
import zipfile
import xmltodict
from datetime import datetime
from tavis.backend.db.utils import get_db_session

def download_extract_zip(url):
  response = requests.get(url,verify=False)
  with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
    for zipinfo in thezip.infolist():
      with thezip.open(zipinfo) as thefile:
        return thefile.read()

def xml_prep(url,zip=True):
  if zip:
    data = download_extract_zip(url)
  else:
    data = requests.get(url,verify=False).text
  return xmltodict.parse(result)

class FeedManager(object):
  """FeedManager base class"""
  def __init__(self, url, feed_type,meta_url=None):
    self.url = url
    self.feed_data_raw = None
    self.feed_type = feed_type
    self.meta_url = meta_url
    self.meta_dict = {}
    self.meta_raw = None
    self.safe_mode = False
    self.outdated = False

  def meta_parse(self):
    meta_data = requests.get(self.meta_url)
    if meta_data.status_code != 200:
      raise Exception('Meta url returned non-200 response code')
    self.meta_raw = meta_data.text
    for l in self.meta_raw.strip().split('\r\n'):
      x = l.split(':',maxsplit=1)
      self.meta_dict[x[0]] = x[1]
      
      if x[0] == 'lastModifiedDate':
        #format fix for 3.6 timezone, fixed in python 3.7
        self.meta_dict[x[0]] = ':'.join(self.meta_dict[x[0]].split(':')[:-1])+self.meta_dict[x[0]].split(':')[-1]
        self.meta_dict[x[0]] = datetime.strptime(self.meta_dict[x[0]],'%Y-%m-%dT%H:%M:%S%z')
      #print('{}: {}'.format(x[0], x[1]))

    