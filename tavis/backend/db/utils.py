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