#! /usr/bin/python
#-*- coding:utf-8 -*-
import time, requests, json
import tornado.web
from utils.log import logger
from utils.dispatcher import MethodDispatcher
from utils.client_manager import client_get
from tornado.concurrent import run_on_executor
from concurrent.futures.thread import ThreadPoolExecutor
from utils.mathpix import handle_pdf, handle_search
from utils.math_logic import handle_logic
from utils.tools import dump_json
# from utils.tex import hanld_tex
from minio import Minio

client = Minio('ele.ink:19000',access_key='admin_minio',secret_key='admin_minio',secure=False)

class AIGCService(MethodDispatcher):
    executor = ThreadPoolExecutor(10)

    def upload_doc(self):
        data = self.request.arguments if self.request.arguments else self.request.body.decode('utf-8')
        if type(data) == str:
            data = json.loads(data)

        request_id, callback_url = data.get("request_id", ""), data.get("callback_url", "")
        file_path, file_type = data.get("file_path", ""), data.get("file_type", "")
        logger.info("request-id:{}, file_path:{}, file_type:{}".format(request_id, file_path, file_type))
        if len(request_id) == 0:
            self.set_status(500)
            data = {"msg": "request_id is empty or callback_url is empty"}      
            self.write(json.dumps(data))
            return

        if len(file_path) == 0 or len(file_type) == 0:
            self.set_status(500)
            data = {"msg": "file_path is empty or file_type is empty"}      
            self.write(json.dumps(data))
            return

        if file_type == "pdf":
            pdf_id = handle_pdf(request_id, file_path, callback_url)
            if pdf_id is None:
                data = {"msg": "handle pdf error"}
                self.set_status(500)
                self.json.dumps(data)
            else:
                url = client.presigned_get_object("data", pdf_id + ".html")
                data = {"request_id":request_id, "status": "ok", "url": url, "bucket": "data", "file_name": pdf_id + ".html"}

        # else:
        #     data = handle_text(request_id, file_path, callback_url)

        self.write(json.dumps(data))
        return

    def search(self):
        data = self.request.arguments if self.request.arguments else self.request.body.decode('utf-8')
        if type(data) == str:
            data = json.loads(data)

        data = {key:data[key].decode("utf-8") for key in data.keys()}
        logger.info("req is {}".format(data))
        text, pdf_id = str(data.get("text", "")), str(data.get("pdf_id", ""))
        request_id, search_type = data.get("request_id", ""), data.get("search_type", "search")
        logger.info("request-id:{}, text:{}, search_type:{}".format(request_id, text, search_type))
        if len(request_id) == 0:
            self.set_status(500)
            data = {"msg": "request_id is empty"}       
            self.write(json.dumps(data))
            return

        if len(text) == 0 or len(search_type) == 0:
            self.set_status(500)
            data = {"msg": "text is empty or search_type is empty"}     
            self.write(json.dumps(data))
            return

        if search_type == "search":
            result = handle_search(request_id, pdf_id, text)
            self.write(json.dumps(result))

    def query(self):
        data = self.request.arguments if self.request.arguments else self.request.body.decode('utf-8')
        if type(data) == str:
            data = json.loads(data)

        dump_json("query.json", data)
        result = {"status": "ok"}
        self.write(json.dumps(result))

    def vote(self):
        data = self.request.arguments if self.request.arguments else self.request.body.decode('utf-8')
        if type(data) == str:
            data = json.loads(data)

        result = yield self.handle(data, True)
        self.write(json.dumps(result))


    @run_on_executor
    def handle(self, data:dict)->dict:
        result = {"math": "", "logic": "", "doc": "", "search_type": data.get("search_type", "")}
        request_id, user_text, search_type = data.get("request_id", ""), data.get("text", ""), data.get("search_type", "")
        start = time.time()

        if search_type == "logic":
            text = handle_logic(user_text)
            if text is None:
                result["msg"] = "handle internal error"
                self.set_status(500)
                return result
            result["logic"] = text
        elif search_type == "search":
            pass
        elif search_type == "math":
            pass
        else:
            self.set_status(500)
            result["msg"] = "unknown search type"

        print(time.time() - handle_start)
        logger.info("handle cost is  {}, result: {}".format(time.time() - start, result))
        return result


url = [
    (r'/aigc/.*', AIGCService),
]

application = tornado.web.Application(
    handlers = url,
)
