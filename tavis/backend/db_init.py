#!/usr/bin/env python

"""
Created by Anthony Velardi on 10/25/18

"""
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import scoped_session
from backend.db.models import *

def get_db(ref='main'):
  dbstring = 'mysql+pymysql://tony:DevPassword1!@127.0.0.1/tavis'
  if dbstring:
    return create_engine(dbstring)
  else:
    return "broke"

def make_tables(base=Base):
  e = get_db()
  base.metadata.create_all(e)

def get_db_session():
    engine = get_db()
    Base.metadata.bind = engine
    dbsession = scoped_session(sessionmaker(bind=engine))
    return dbsession()

make_tables()