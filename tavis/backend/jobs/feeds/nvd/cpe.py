#!/usr/bin/env python

'''
CPE feed management
'''

from tavis.backend.jobs.feeds.utils import FeedManager

class CPE_Feed(FeedManager):
  def __init__(self,url=None,feed_type=None):
    self.url = 'https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.zip'
    self.feed_type='cpe'
    self.meta_url = 'https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.meta'
    FeedManager.__init__(self,self.url,self.feed_type,meta_url=self.meta_url)