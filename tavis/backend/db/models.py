#!/usr/bin/env python

"""
Created by Anthony Velardi on 10/25/18

"""

from sqlalchemy import Column, Table, Integer, String, ForeignKey, Boolean, DateTime, Text, Float, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
import datetime

String = String(length=200)


tablebase = ''

class Base_Table(object):
  @declared_attr
  def __tablename__(cls):
    return tablebase + cls.__name__.lower()
  
  id = Column(Integer, primary_key=True)
  created = Column(DateTime, default=datetime.datetime.now)
  modified = Column(DateTime, onupdate=datetime.datetime.now, default=None)
  
Base = declarative_base(cls=Base_Table)

#object type templates
# class Item_Base_Table(Base):
#   @declared_attr
#   def __tablename__(cls):
#     return tablebase + cls.__name__.lower()
  # name = Column(String)
  # site = Column(String)
  # info = Column(Text)
#   def __repr__(self):
#     return self.name

link_vuln_tag_table = Table('link_vuln_tag',Base.metadata,
    Column('left_id', Integer, ForeignKey('vuln.id')),
    Column('right_id', Integer, ForeignKey('vuln_tag.id'))
)

link_secad_os_table = Table('link_secad_os',Base.metadata,
  Column('left_id',Integer,ForeignKey('security_advisory.id')),
  Column('right_id',Integer,ForeignKey('operating_system.id'))
)

link_secad_distro_table = Table('link_secad_distro',Base.metadata,
  Column('left_id',Integer,ForeignKey('security_advisory.id')),
  Column('right_id',Integer,ForeignKey('distro.id'))
)

link_secad_distroversion_table = Table('link_secad_distroversion',Base.metadata,
  Column('left_id',Integer,ForeignKey('security_advisory.id')),
  Column('right_id',Integer,ForeignKey('distro_version.id'))
)

link_secad_cve_table = Table('link_secad_cve',Base.metadata,
  Column('left_id',Integer,ForeignKey('security_advisory.id')),
  Column('right_id',Integer,ForeignKey('cve_number.id'))
)


link_secad_vuln_table = Table('link_secad_vuln',Base.metadata,
  Column('left_id',Integer,ForeignKey('security_advisory.id')),
  Column('right_id',Integer,ForeignKey('vuln.id'))
)

link_vuln_os_table = Table('link_vuln_os',Base.metadata,
  Column('left_id',Integer,ForeignKey('vuln.id')),
  Column('right_id',Integer,ForeignKey('operating_system.id'))
)

link_vuln_distro_table = Table('link_vuln_distro',Base.metadata,
  Column('left_id',Integer,ForeignKey('vuln.id')),
  Column('right_id',Integer,ForeignKey('distro.id'))
)

link_vuln_distro_version_table = Table('link_vuln_distro_version',Base.metadata,
  Column('left_id',Integer,ForeignKey('vuln.id')),
  Column('right_id',Integer,ForeignKey('distro_version.id'))
)

link_vuln_package_table = Table('link_vuln_package',Base.metadata,
  Column('left_id',Integer,ForeignKey('vuln.id')),
  Column('right_id',Integer,ForeignKey('linux_package.id'))
)

link_vuln_link_feed_table = Table('link_vuln_link_feed',Base.metadata,
  Column('left_id',Integer,ForeignKey('vuln_link.id')),
  Column('right_id',Integer,ForeignKey('vuln_feed.id'))
)

link_cpe_version_distro_table= Table('link_cpe_version_distro',Base.metadata,
  Column('left_id',Integer,ForeignKey('cpe_version.id')),
  Column('right_id',Integer,ForeignKey('distro.id'))
)

link_cpe_version_distro_version_table= Table('link_cpe_version_distro_version',Base.metadata,
  Column('left_id',Integer,ForeignKey('cpe_version.id')),
  Column('right_id',Integer,ForeignKey('distro_version.id'))
)

link_cpe_version_os_table= Table('link_cpe_version_os',Base.metadata,
  Column('left_id',Integer,ForeignKey('cpe_version.id')),
  Column('right_id',Integer,ForeignKey('operating_system.id'))
)


link_cpe_version_url_table= Table('link_cpe_version_url',Base.metadata,
  Column('left_id',Integer,ForeignKey('cpe_version.id')),
  Column('right_id',Integer,ForeignKey('cpe_link.id'))
)

link_cpe_vendor_url_table= Table('link_cpe_vendor_url',Base.metadata,
  Column('left_id',Integer,ForeignKey('cpe_vendor.id')),
  Column('right_id',Integer,ForeignKey('cpe_link.id'))
)

link_cpe_product_url_table= Table('link_cpe_product_url',Base.metadata,
  Column('left_id',Integer,ForeignKey('cpe_product.id')),
  Column('right_id',Integer,ForeignKey('cpe_link.id'))
)





class Vuln(Base):
  cves = relationship("CVE_Number",backref='Vuln')
  vendor = Column(Integer, ForeignKey('cpe_vendor.id'))
  product = Column(Integer, ForeignKey('cpe_product.id'))
  versions = relationship("Software_Version",backref='Vuln')
  title = Column(Integer,ForeignKey('vuln_title.id'))
  advisories = relationship("Security_Advisory",secondary=link_secad_vuln_table,back_populates="vulns")
  operating_systems = relationship("Operating_System",secondary=link_vuln_os_table,back_populates='vulns')
  distros = relationship("Distro",secondary=link_vuln_distro_table,back_populates='vulns')
  distro_versions = relationship("Distro_Version",secondary=link_vuln_distro_version_table,back_populates='vulns')
  packages = relationship("Linux_Package",secondary=link_vuln_package_table,back_populates='vulns')
  category = Column(Integer)
  
  
class Vuln_Title(Base):
  vuln = Column(Integer, ForeignKey('vuln.id'))
  text = Column(String)
  
class Vuln_Link(Base):
  vuln = Column(Integer, ForeignKey('vuln.id'))
  cve = Column(Integer, ForeignKey('cve_number.id'))
  url = Column(String)
  title = Column(String)
  description = Column(Text)
  feeds = relationship('Vuln_Feed',secondary=link_vuln_link_feed_table,back_populates='vuln_links')
  
class Vuln_Feed(Base):
  url = Column(String)
  title = Column(String)
  description = Column(Text)
  vendor = Column(Integer,ForeignKey('cpe_vendor.id'))
  links = relationship('Vuln_Link',secondary=link_vuln_link_feed_table,back_populates='vuln_feeds')


class CVE_Number(Base):
  vuln = Column(Integer, ForeignKey('vuln.id'))
  cve = Column(String,nullable=False)
  # links = relationship("CVE_Link",backref='CVE_Number')
  vendor = Column(Integer, ForeignKey('cpe_vendor.id'))
  product = Column(Integer, ForeignKey('cpe_product.id'))
  versions = relationship("Version",backref='CVENumber')
  cvssv3 = Column(Float)
  cvssv2 = Column(Float)
  package = Column(Integer,ForeignKey('linux_package.id'))
  pubday = Column(Integer)
  pubmonth = Column(Integer)
  pubyear = Column(Integer)
  security_advisories = relationship("Security_Advisory",secondary=link_secad_cve_table,back_populates='cve_numbers')
  def __repr__(self):
      return self.cve

class CPE_Version(Base):
  vulns = relationship("Vuln",backref='CPE_Version')
  status = Column(Integer)#0=vuln,1=fixed
  version = Column(String)
  product = Column(Integer,ForeignKey('cpe_product.id'))
  vendor = Column(Integer,ForeignKey('cpe_vendor.id'))
  os = Column(Integer,ForeignKey('operating_system.id'))
  distros = relationship('Distro',secondary=link_cpe_version_distro_table,backref='cpe_version')
  distro_versions = relationship('Distro_Version',secondary=link_cpe_version_distro_version_table,backref='cpe_version')
  version_number = Column(String)
  nvd_mod_dt = Column(String)
  nvd_status = Column(String)
  nvd_id = Column(Integer)
  title = Column(String)
  cpe_string = Column(String)
  cpe_links = relationship("CPE_Link",secondary=link_cpe_version_url_table,back_populates="cpe_versions")

class Operating_System(Base):
  name = Column(String)
  link = Column(String)
  vendor = Column(Integer,ForeignKey('cpe_vendor.id'))
  description = Column(Text)
  distros = relationship("Distro")

class Distro(Base):
  operating_system = Column(Integer,ForeignKey('operating_system.id'))
  versions = relationship("Distro_Version",backref='distro')
  eol_dt = Column(DateTime,default=None)
  eol_bool=Column(Boolean,default=False)
  
class Distro_Version(Base):
  code_name = Column(String)
  operating_system = Column(Integer, ForeignKey('operating_system.id'))
  distro = Column(Integer,ForeignKey('distro.id'))

class Linux_Package(Base):
  os = Column(Integer,ForeignKey('operating_system.id'))
  distro_version = Column(Integer,ForeignKey('distro_version.id'))
  name = Column(String)
  link = Column(String)
  seclink = Column(String)
  product = Column(Integer, ForeignKey('cpe_product.id'))

class CPE_Product(Base):
  cves = relationship('CVE_Number', backref='CPE_Product')
  vendor = Column(Integer,ForeignKey('cpe_vendor.id'))
  versions = relationship('CPE_Version',backref='CPE_Product')
  name = Column(String)
  site = Column(String)
  info = Column(Text)
  cpe_links = relationship("CPE_Link",secondary=link_cpe_product_url_table,back_populates="cpe_products")

class CPE_Vendor(Base):
  vulns = relationship('Vuln',backref='CPE_Vendor')
  products = relationship('Product', backref='CPE_Vendor')
  name = Column(String)
  site = Column(String)
  info = Column(Text)
  cpe_links = relationship("CPE_Link",secondary=link_cpe_vendor_url_table,back_populates="cpe_vendors")

class CPE_Link(Base):
  category = Column(String)
  url = Column(String)
  cpe_versions = relationship("CPE_Version",secondary=link_cpe_version_url_table,back_populates="cpe_links")
  cpe_vendors = relationship("CPE_Vendor",secondary=link_cpe_vendor_url_table,back_populates="cpe_links")
  cpe_products = relationship("CPE_Product",secondary=link_cpe_product_url_table,back_populates="cpe_links")
  
class Vuln_Text(Base):
  text = Column(Text)
  cve = Column(Integer, ForeignKey('vuln.id'))

class Security_Advisory(Base):
  title = Column(String)
  description = Column(Text)
  operating_systems = relationship('Operating_System',secondary=link_secad_os_table,back_populates="security_advisories")
  distros = relationship("Distro",secondary=link_secad_distro_table,back_populates="security_advisories")
  distro_versions = relationship("Distro_Version",secondary=link_secad_distroversion_table,back_populates="security_advisories")
  cve_numbers = relationship("CVE_Number",secondary=link_secad_cve_table,back_populates="security_advisories")
  vulns = relationship("Vuln",secondary=link_secad_vuln_table,back_populates="security_advisories")

class Vuln_Tag(Base):
  name = Column(String)
  vuln = relationship("Vuln",secondary=link_vuln_tag_table,back_populates="tags")

class Vuln_Note(Base):
  user = Column(Integer,default=0)
  vuln = Column(Integer, ForeignKey('vuln.id'))
  title = Column(String)
  body = Column(Text)
  body_format = Column(Integer,default=0) #future markdown support

class Feed_Log(Base):
  url = Column(String)
  version_before = Column(String)
  version_after = Column(String)
  progress = Column(Integer)
  success = Column(Boolean)
  update_req = Column(Boolean)
  info = Column(Text)

class Feed_Status(Base):
  info = Column(Text)
  feed_type = Column(Integer)
  feed_id = Column(String)
  url = Column(String)
  meta_url = Column(String)
  last_success = Column(DateTime)
  last_failure = Column(DateTime)
  last_db_update = Column(DateTime)
  job_start_dt = Column(DateTime)
  job_running = Column(Boolean,default=False)
  db_version =- Column(String)

class Feed_URL(Base):
  url = Column(String)
  url_type = Column(Integer,default=0)


class Feed_Meta_Info(Base):
  url = Column(Integer,ForeignKey('feed_url.id'))
  remote_update = Column(DateTime)
  db_update = Column(DateTime)
  


