#!/usr/bin/env python

"""
Created by Anthony Velardi on 11/2/18

"""
from tavis.utils.data import vuln_dict

def parse_cpe(cpe_string):
  cpe_string = cpe_string.split(':')
  if cpe_string[0] != 'cpe':
    raise Exception('CPE string doesnt appear compliant')
  update = None
  part = cpe_string[1][-1]
  vendor = cpe_string[2]
  product = cpe_string[3]
  version = cpe_string[4]
  if len(cpe_string) > 5:
    #check for stuff we want to ignore
    if cpe_string[5] not in ['-']:
      update = cpe_string[5]
  return {
    'part': part,
    'vendor': vendor,
    'product': product,
    'version': version,
    'update': update
  }

def generate_cpe_dict(cpe_string_list):
  master = vuln_dict()
  for item in cpe_string_list:
    cpe_dict = parse_cpe(item)
    if cpe_dict['vendor'] not in master['vendor']:
      master['vendor'][cpe_dict['vendor']] = {
        'product': {
          cpe_dict['product']: {
            'version': {
              cpe_dict['version']: {
                'update': {
                  cpe_dict['update']
                }
                
              }
            }
          }
        }
      }
      if cpe_dict['update']:
        master['vendor'][cpe_dict['vendor']] = {
          'product': {
            cpe_dict['product']: {
              'version': {
                cpe_dict['version']: {
                  'update': {
                    cpe_dict['update']: {}
                  }
                }
              }
            }
          }
        }
    elif cpe_dict['product'] not in master['vendor'][cpe_dict['vendor']]['product']:
      master['vendor'][cpe_dict['vendor']]['product'][cpe_dict['product']] = {
          'version':{
            cpe_dict['version']:{
              'update':{
                cpe_dict['update']: {}
              }
            }
          }
        }
    elif cpe_dict['version'] not in master['vendor'][cpe_dict['vendor']]['product'][cpe_dict['product']]['version']:
      master['vendor'][cpe_dict['vendor']]['product'][cpe_dict['product']]['version'][cpe_dict['version']] = {
        'update': {
          cpe_dict['update'] : {}
        }
      }
    elif cpe_dict['update'] not in master['vendor'][cpe_dict['vendor']]['product'][cpe_dict['product']]['version'][cpe_dict['version']]['update']:
      master['vendor'][cpe_dict['vendor']]['product'][cpe_dict['product']]['version'][cpe_dict['version']]['update']: {
        cpe_dict['update']: {}
      }
  return master
  