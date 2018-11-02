#!/usr/bin/env python


import requests
import io
import zipfile
import pdb
import xmltodict

def download_extract_zip(url):
  response = requests.get(url,verify=False)
  with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
    for zipinfo in thezip.infolist():
      with thezip.open(zipinfo) as thefile:
        return thefile.read()



print('Welcome!')
result = download_extract_zip('https://nvd.nist.gov/feeds/xml/cpe/dictionary/archive-official-cpe-dictionary_v2.2-20181025-000915.xml.zip')
cpe_dict = xmltodict.parse(result)
for x in cpe_dict['cpe-list']['cpe-item']:
  print(x)
