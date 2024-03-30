#! /usr/bin/python
#-*- coding:utf-8 -*-
import time, requests, json
import tornado.web
from utils.log import logger
from utils.dispatcher import MethodDispatcher
from utils.client_manager import client_get
from tornado.concurrent import run_on_executor
from concurrent.futures.thread import ThreadPoolExecutor
from utils.mathpix import handle_pdf, handle_search, handle_batch, get_pdf_ids
from utils.tools import dump_json
# from utils.tex import hanld_tex
from minio import Minio

# ------------------------------------- - ------------------------------------ #
from ananke.llm.azure import Azure
from ntptutorial.partII_dsp.solver_beta import MathTheoremProvingService


client = Minio('ele.ink:19000',access_key='admin_minio',secret_key='admin_minio',secure=False)
openai_model=Azure(chat_model_name="Ananke3-1106-US-WEST")
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


    def pdfs(self):
        data = self.request.arguments if self.request.arguments else self.request.body.decode('utf-8')
        if type(data) == str and len(data) != 0:
            data = json.loads(data)

        if len(data) == 0:
            data = {}

        data = {key:data[key].decode("utf-8") for key in data.keys()}
        request_id = data.get("request_id", "just a get req")
        logger.info("request-id is {}".format(request_id))
        tenant = data.get("tenant", "all")
        result = get_pdf_ids(request_id, tenant)
        self.write(json.dumps(result))


    def upload_batch(self):
        data = self.request.arguments if self.request.arguments else self.request.body.decode('utf-8')
        if type(data) == str:
            data = json.loads(data)

        request_id, file_paths, tenant = data.get("request_id"), data.get("file_paths"), data.get("tenant", "all")
        pdf_ids = handle_batch(request_id, file_paths, tenant)
        self.write(json.dumps({"request_id": request_id, "pdfs": pdf_ids, "bucket": "data"}))

    @run_on_executor
    def handle(self, data:dict)->dict:
        result = {}
        return result

    @run_on_executor
    def async_search(self, **data):
        request_id = data.get("request_id", "default_request")
        text = data.get("user_text")

        result = handle_search(request_id, "", text)
        return result

    @run_on_executor
    def code_agent(self):
        data = self.request.arguments if self.request.arguments else self.request.body.decode('utf-8')
        if type(data) == str:
            data = json.loads(data)
        """ 
        Not Support Streaming mode
        """
        result={"code_agent":"not support this version"}
        return result
            
            

    @run_on_executor
    def math_solver(self, **data):
        informal_statement=data.get("informal_statement")
        formal_statement=data.get("formal_statement")
        isa_path='/root/Isabelle2022'
        theory_file='/root/Isabelle2022/src/HOL/Examples/Interactive.thy'
        port=8051
        service = MathTheoremProvingService(isa_path, theory_file, port)

        theorem_with_proof = service.generate_draft_sketch(informal_statement, formal_statement)

        
        result = service.check_conjectures(theorem_with_proof)
        if result['success']:
                print("Proof successful:")
                print(result['theorem_and_proof'])
        else:
                print("Proof failed.")
        

        result = {"status":result['success'],"math_solver":result['theorem_and_proof']}
        return result


    @run_on_executor
    def generate(self, **data):
        user_context=data.get("user_text")
        result_context=openai_model.chat(user_context)
        result = {"generate":result_context}
        return result

    def get_intention(self, user_context):
        # from UserContext to Certainly pipeline
        # curl -X POST 'https://api.dify.ai/v1/chat-messages' \
        # --header 'Authorization: Bearer app-4sHHrCOb1jLDfGDwcFLFbLUm' \
        # --header 'Content-Type: application/json' \
        # --data-raw '{
        #     "inputs": {},
        #     "query": "What are the specs of the iPhone 13 Pro Max?",
        #     "response_mode": "blocking",
        #     "conversation_id": "",
        #     "user": "tomwinshare@gmail.com"
        # }'
        
        import requests

        # 设置API端点
        url = 'https://api.dify.ai/v1/chat-messages'
        # 设置请求头
        headers = {
            'Authorization': 'Bearer app-4sHHrCOb1jLDfGDwcFLFbLUm',
            'Content-Type': 'application/json'
        }

        # 设置请求体
        dify_data = {
            "inputs": {},
            "query": user_context,
            "response_mode": "blocking",
            "conversation_id": "",
            "user": "tomwinshare@gmail.com"
        }

        # 发送POST请求
        response = requests.post(url, headers=headers, json = dify_data)
        response_dict = json.loads(response.content)
        answer = response_dict.get("answer")
        logger.info("answer type is {}".format(type(answer)))
        if type(answer) == str:
            answer = json.loads(answer)
        answer = answer.get("type")
        logger.info("answer is {}".format(answer))
        if answer is None:
            answer = "search"
        return answer

    def intention_split(self):
        data = self.request.arguments if self.request.arguments else self.request.body.decode('utf-8')
        if type(data) == str:
            data = json.loads(data)

        logger.info("req is {}".format(data))
        request_id, user_context = data.get("request_id"), data.get("user_text")
        functional_dict = {
            "search": self.async_search,
            "code_agent": self.code_agent,
            "math_solver":self.math_solver,
            "generate":self.generate
        }
        
        intention = self.get_intention(user_context)
        intention_result = yield functional_dict.get(intention, self.async_search)(**data)
        result = {intention: intention_result}
        self.write(json.dumps(result))
        return

url = [
    (r'/aigc/.*', AIGCService),
]

application = tornado.web.Application(
    handlers = url,
)
