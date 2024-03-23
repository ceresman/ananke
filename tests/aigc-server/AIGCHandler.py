#! /usr/bin/python
#-*- coding:utf-8 -*-
import time, requests, json
import tornado.web
from utils.log import logger
from utils.dispatcher import MethodDispatcher
from utils.client_manager import client_get
from tornado.concurrent import run_on_executor
from concurrent.futures.thread import ThreadPoolExecutor

class AIGCService(MethodDispatcher):
	executor = ThreadPoolExecutor(10)

	def upload_doc(self):
		data = self.request.arguments if self.request.arguments else self.request.body.decode('utf-8')
		if type(data) == str:
			data = json.loads(data)

		request_id, callback_url = data.get("request_id", ""), data.get("callback_url", "")
		file_path, file_type = data.get("file_path", ""), data.get("file_type", "")
		logger.info("request-id:{}, file_path:{}, file_type:{}".format(request_id, file_path, file_type))
		if len(request_id) == 0 or len(callback_url) == 0:
			self.set_status(500)
			data = {"msg": "request_id is empty or callback_url is empty"}		
			self.write(json.dumps(data))

		if len(file_path) == 0 or len(file_type) == 0:
			self.set_status(500)
			data = {"msg": "file_path is empty or file_type is empty"}		
			self.write(json.dumps(data))

		data = {}
		self.write(json.dumps(data))

	def search(self):
		data = self.request.arguments if self.request.arguments else self.request.body.decode('utf-8')
		if type(data) == str:
			data = json.loads(data)

		request_id, text, search_type = data.get("request_id", ""), data.get("text", ""), data.get("search_type", "")
		logger.info("request-id:{}, text:{}, search_type:{}".format(request_id, file_path, search_type))
		if len(request_id) == 0:
			self.set_status(500)
			data = {"msg": "request_id is empty"}		
			self.write(json.dumps(data))

		if len(text) == 0 or len(search_type) == 0:
			self.set_status(500)
			data = {"msg": "text is empty or search_type is empty"}		
			self.write(json.dumps(data))

		result = yield self.handle(data)
		self.write(json.dumps(result))

	def query(self):
		data = self.request.arguments if self.request.arguments else self.request.body.decode('utf-8')
		if type(data) == str:
			data = json.loads(data)
		result = yield self.handle(data, False)
		self.write(json.dumps(result))

	def vote(self):
		data = self.request.arguments if self.request.arguments else self.request.body.decode('utf-8')
		if type(data) == str:
			data = json.loads(data)

		result = yield self.handle(data, True)
		self.write(json.dumps(result))


	@run_on_executor
	def handle(self, req_data:dict)->dict:
		return {"houyu": "hy"}
		handle_start = time.time()
		print(time.time() - handle_start)
		logger.info("result: {}".format(result))
		return result


url = [
    (r'/aigc/.*', AIGCService),
]

application = tornado.web.Application(
    handlers = url,
)
