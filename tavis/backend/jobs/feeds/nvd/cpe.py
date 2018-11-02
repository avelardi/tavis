#!/usr/bin/env python

'''
CPE feed management
'''

from tavis.backend.jobs.feeds.utils import FeedManager
from tavis.utils.data import vuln_dict

class CPE_Feed(FeedManager):
  def __init__(self,url=None,feed_type=None):
    self.url = 'https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.zip'
    self.feed_type=0
    self.meta_url = 'https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.meta'
    FeedManager.__init__(self,self.url,self.feed_type,meta_url=self.meta_url)
  
  def parse_feed(self):
    self.data_parse()
    self.feed_dict = vuln_dict()
    for item in self.feed_data_parsed['cpe-list']['cpe-item']:
      print(item['@name'])
    
      
    
  