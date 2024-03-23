#! /usr/bin/python
#-*- coding:utf-8 -*-
import json,yaml, requests
import os, time, sys
from pathlib import Path
from utils.log import logger
from utils.client_manager import client_get
from rediscluster import RedisCluster

def load_yaml(path_dir):
	data = {}
	with open(path_dir, 'r') as f:
		data = yaml.load(f.read())
	return data

def dump_json(path_dir, data:dict):
	with open(path_dir, 'w+', encoding='utf8') as fp:
		json.dump(data, fp, ensure_ascii=False, indent = 4)

def init_redis(startup_nodes:list, password:str):
	try:
		redic_conn = RedisCluster(startup_nodes = startup_nodes, skip_full_coverage_check = True,
				decode_responses = True, password = password)
	except Exception as e:
		logger.error("rediscluster init failed!")
		sys.exit(1)

	logger.info("rediscluster init success!")
	return redic_conn

def init_kafka(cluster_nodes:list, ):
	try:
		kafka_producer = KafkaProducer(bootstrap_servers = cluster_nodes)
	except Exception as e:
		logger.error("KafkaProducer init failed!")
		sys.exit(1)

	logger.info("KafkaProducer init success!")
	return kafka_producer

def write_redis(key, value, ex_time = 450):
	rc = client_get("redis")
	# rc.setex(key, value, ex_time)
	print(key)
	rc.setex(key, ex_time, value)
	# rc.set(key, value)

def read_redis(key)->dict:
	rc = client_get("redis")
	value = rc.get(key)
	# value = rc.get(key).decode(encoding="utf-8")
	try:
		return json.loads(value)
	except Exception as e:
		logger.error("read_redis use {} error: {}".format(key))
		return None
