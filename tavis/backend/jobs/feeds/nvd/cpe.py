#!/usr/bin/env python

'''
CPE feed management
'''

from tavis.backend.jobs.feeds.utils import FeedManager
from tavis.backend.jobs.feeds.nvd.utils import generate_cpe_dict
from tavis.backend.db.utils import add_missing_cpe_vendor,add_missing_cpe_product
from tavis.backend.db.utils import get_db_session

class CPE_Feed(FeedManager):
  def __init__(self,url=None,feed_type=None):
    self.url = 'https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.zip'
    self.feed_type=0
    self.meta_url = 'https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.meta'
    FeedManager.__init__(self,self.url,self.feed_type,meta_url=self.meta_url)
  
  def parse_feed(self):
    self.data_parse()
    session = get_db_session()
    self.feed_dict = generate_cpe_dict([x['@name'] for x in self.feed_data_parsed['cpe-list']['cpe-item']])
    add_missing_cpe_vendor(self.feed_dict,session)
    print('Vendor check complete')
    for vendor in self.feed_dict['vendor']:
      if 'product' in self.feed_dict['vendor'][vendor]:
        add_missing_cpe_product(self.feed_dict['vendor'][vendor]['product'],vendor,session)
    
      
      
      
      
      
    
  