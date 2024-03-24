#! /usr/bin/python
#-*- coding:utf-8 -*-
from utils.log import logger
from utils.tools import load_yaml, init_redis, init_kafka
from utils.client_manager import client_init, client_set, client_get
from AIGCHandler import application
import tornado
import yaml

config_dir = "/mnt/e/sides/ananke/aigc-server/etc/config.yaml"

def load_yaml(path_dir):
	data = {}
	with open(path_dir, 'r') as f:
		data = yaml.load(f.read(), Loader = yaml.Loader)
	return data


if __name__	 == "__main__":
	# client_init()
	config = load_yaml(config_dir)
	logger.info("config is {}".format(config))
	# config = {}
	redis_conn = init_redis(config.get("redis-cluster"), config.get("redis-password"))

	# assert(redis_conn != None)

	# client_set("config", config)
	client_set("redis", redis_conn)
	# client_set("kafka_appName", config.get("kafka_appName"))
	# client_set("kafka_appToken", config.get("kafka_appToken"))
	# client_set("kafka_appTopic", config.get("kafka_appTopic"))
	# client_set("kafka_url", config.get("kafka_url"))

	logger.info("BotApiGateWay server start begin!")
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.bind(config.get("port", 18080))
	http_server.start(0)
	logger.info("BotApiGateWay server start end!")
	tornado.ioloop.IOLoop.instance().start()
