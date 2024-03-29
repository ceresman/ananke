#! /usr/bin/python
#-*- coding:utf-8 -*-
from ananke.data.math_logic import Logic
from utils.log import logger

dic = {
  "api_key":"61bc1aab37364618ae0df70bf5f340dd",
  "api_version":"2024-02-15-preview",
  "endpoint":"https://anankeus.openai.azure.com/",
  "kg_host": "localhost",
  "kg_port": "7687",
  "kg_user": "neo4j",
  "kg_passwd": "123456", 
  "kg_db": "neo4j"
}

logic = Logic(**dic)

def handle_logic(text:str):
    try:
        response  = logic.handle_logic(text)
        return reponse
    except Exception as e:
        logger.error("handle logic error, {}".format(e))
        return None