#! /usr/bin/python
#-*- coding:utf-8 -*-
from utils.log import logger
from utils.tools import load_yaml, init_redis_single
from utils.client_manager import client_init, client_set, client_get
from AIGCHandler import application
import tornado, os, yaml
import yaml
from utils.mathpix import handle_search

config_dir = os.environ.get("SERVER_CONFIG")

def load_yaml(path_dir):
	if path_dir is None:
		logger.info("config path is None")
		exit(1)

	data = {}
	with open(path_dir, 'r') as f:
		data = yaml.load(f.read(), Loader = yaml.Loader)
	return data


if __name__	 == "__main__":
	client_init()
	config = load_yaml(config_dir)
	logger.info("config is {}".format(config))
	redis_conn = init_redis_single(config.get("redis-hostport"), config.get("redis-password"))

	assert(redis_conn != None)

	# redis_conn.flushall()
	client_set("redis", redis_conn)
	client_set("config", config)
	logger.info("ApiGateWay server start begin!")
	logger.info("redis ping is {}".format(redis_conn.ping()))
	pdf_id = "2024_03_28_d918ce007641daed7730g"
	user_text = "machine learning"
	# user_text = 'Machine Learning Algorithm'
	# user_text = "classification"
	result = handle_search("11111111", pdf_id, user_text)
	metas = result.get("self").get("metas")	
	print(metas)