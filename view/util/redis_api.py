#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
File Name : 'redis_api'.py 
Description:
Author: 'zhengyang' 
Date: '2017/3/7' '15:43'
"""
import redis
import configparser
from hashlib import md5

cp = configparser.SafeConfigParser()
cp.read('/usr/lxw/explore/model/db_conf')

host = cp.get('redis-db', 'REDIS_HOST')
port = cp.get('redis-db', 'REDIS_PORT')
password = cp.get('redis-db', 'REDIS_PWD')
db_distinct = cp.get('redis-db', 'REDIS_DB_DISTINCT')
redis_set_name = cp.get('redis-db', 'REDIS_SET_NAME')

# 去重
pool_3 = redis.ConnectionPool(host=host, port=port, db=db_distinct)
r_distinct = redis.StrictRedis(connection_pool=pool_3)


def get_hash_value(value):
    m = md5()
    m.update(value.encode('utf-8'))
    hash_value = m.hexdigest()
    return hash_value


def exists_url_hash(value, r=r_distinct, set_name=redis_set_name):
    hash_value = get_hash_value(value)
    result = r.sismember(set_name, hash_value)
    return result


def remove_url_hash(hash_value):
    result = r_distinct.srem(redis_set_name, hash_value)
    return result


def add_url_hash(value, r=r_distinct, set_name=redis_set_name):
    hash_value = get_hash_value(value)
    r.sadd(set_name, hash_value)


if __name__ == "__main__":
    # print is_new(123456)
    add_url_hash('hello world3')
