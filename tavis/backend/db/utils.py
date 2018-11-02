#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import scoped_session
from tavis.backend.db.models import *
from sys import exit

def get_db(dbstring='mysql+pymysql://root:DevPassword1!@127.0.0.1/tavis'):
  
  if dbstring:
    return create_engine(dbstring)
  else:
    print("No DB string passed in, quitting")
    exit()

def make_tables(base=Base):
  e = get_db()
  base.metadata.create_all(e)

def get_db_session():
    engine = get_db()
    Base.metadata.bind = engine
    dbsession = scoped_session(sessionmaker(bind=engine))
    return dbsession()

def add_missing_cpe_vendor(cpe_dict,session):
  for vendor in cpe_dict['vendor']:
    if vendor in ['product','info']:
      continue
    try:
      db_vendor = session.query(CPE_Vendor).filter(CPE_Vendor.name == vendor).first()
    except:
      db_vendor = None
    if not db_vendor:
      print('{} not in DB, adding...'.format(vendor))
      vendor_object = CPE_Vendor(name=vendor,)
      session.add(vendor_object)
    session.commit()

    

def add_missing_cpe_product(product_dict,vendor_name,session):
  vendor_id = session.query(CPE_Vendor).filter(CPE_Vendor.name == vendor_name).first().id
  for product in product_dict:
    try:
      db_product = session.query(CPE_Product).filter(CPE_Product.name == product,CPE_Product.vendor == vendor_id).first()
    except:
      db_product = None
    if not db_product:
      product_object = CPE_Product(name=product,vendor=vendor_id)
      session.add(product_object)
      print('Adding product {}:{}'.format(str(vendor_id),product))
  session.commit()