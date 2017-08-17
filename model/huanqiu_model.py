# -*- coding:utf-8 -*-
"""
File Name: huanqiu
Version:
Description:
Author: liuxuewen
Date: 2017/8/11 10:23
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import configparser

cp = configparser.SafeConfigParser()
cp.read('D:/project/myproject/explore/model/db_conf')

user = cp.get('mysql-db', 'MYSQL_USER')
pwd = cp.get('mysql-db', 'MYSQL_PWD')
host = cp.get('mysql-db', 'MYSQL_HOST')
port = cp.get('mysql-db', 'MYSQL_PORT')
db = cp.get('mysql-db', 'MYSQLS_DB_NAME')
engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(user, pwd, host, port, db),
                       echo=False)
db_session = sessionmaker(bind=engine)()

Base = declarative_base()


class HuanQiuOrm(Base):
    __tablename__ = 'huanqiu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(64))
    link = Column(String(64))
    brief = Column(String(64))
    create_time = Column(DateTime)
    img_url = Column(String(128))
