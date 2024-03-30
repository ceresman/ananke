#! /usr/bin/python
#-*- coding:utf-8 -*-
import requests, json
import threading, time, os
import nltk, spacy
from utils.log import logger
from utils.tools import dump_json
from minio import Minio
from utils.client_manager import client_get
from utils.doc_flow import DocFlow
from utils.tools import init_redis_single

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


client = Minio('ele.ink:19000',access_key='admin_minio',secret_key='admin_minio',secure=False)
doc_flow = DocFlow(**dic)

headers = {
    "app_id": "prismer_eb9b69_0f28c4",
    "app_key": "2796ffd82e527755f9f593ac2091d4bf76036534ca2ca2e39532814f5f75ff00",
    "Content-type": "application/json"
}


def get_redis():
    redis = client_get("redis")
    config = client_get("config")

    while True:
        try:
            redis.ping()
            return redis
        except Exception as e:
            logger.info("redis conn lose, reconnec, exception is {}".format(e))
            time.sleep(3)
            redis = init_redis_single(config.get("redis-hostport"), config.get("redis-password"))
            client_set(redis)

def get_authors(texts):
    authors = []
    nlp = spacy.load("en_core_web_sm")
    for text in texts:
        doc = nlp(text)
        entities = [ent.text for ent in doc.ents]
        person_names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        authors.extend(person_names)
    return authors

def get_page_one(page_one):
    author_flag = True
    author_texts = []
    abstract_ix = -1
    abstract, title = "", ""
    page_text = ""
    for ix, line in enumerate(page_one.get("lines"), start = 0):
        if ix == 0:
            title = line.get('text')
        else:
            if ix > 8:
                page_text = page_text + line.get("text")
            if "abstract" in line.get("text").lower():
                abstract_ix = ix
        
            if abstract_ix != -1 and ix > abstract_ix:
                abstract = abstract + " " + line.get("text")

            if author_flag and abstract_ix == -1:
                author_texts.append(line.get('text'))

    if abstract_ix == -1:
        abstract = page_text

    return title, author_texts, abstract

def process_pdf_by_mathpix(pdf_url):
    url = "https://api.mathpix.com/v3/pdf"
    data = {
        "url": pdf_url,
        "conversion_formats": {
            "docx": True,
            "tex.zip": True,
            "html": True
        }
    }
    logger.info("mathpix-req: {}".format(data))
    for i in range(0 , 3):
        try:
            req = requests.post(url, json = data, headers = headers)
            return json.loads(req.content)
        except Exception as err:
            logger.info("process_pdf_error:code {}, msg: {}".format(req.status_code, req.content))
            continue

def retry_get(url, headers):
    for i in range(0, 5):
        try:
            req = requests.get(url, headers = headers)
            return json.loads(req.content)
        except Exception as e:
            logger.info("get url-{} exception {}".format(url, e))
            time.sleep(3)

    logger.error("failed to request mathpix")
    return {}

def get_process_status(pdf_id):
    url = "https://api.mathpix.com/v3/pdf/{}".format(pdf_id)
    return retry_get(url, headers)

def get_conversion_status(pdf_id):
    url = "https://api.mathpix.com/v3/converter/{}".format(pdf_id)
    return retry_get(url, headers)

def get_pdf_html_data(pdf_id):
    url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".html"
    for i in range(0, 5):
        try:
            response = requests.get(url, headers = headers)
            with open(pdf_id + ".html", "wb") as f:
                f.write(response.content)
            return (response.content)
        except Exception as e:
            logger.info("get url-{} exception {}".format(url, e))
            time.sleep(3)

    logger.error("failed to request mathpix")
    return {}

def get_pdf_lines_data(pdf_id):
    url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".lines.json"
    return retry_get(url, headers)

def get_page_data(lines_data):
    page_data = {}
    for page in lines_data.get("pages", []):
        page_text = ""
        page_id = page.get("page")
        lines = page.get("lines", [])
        for line in lines:
            page_text = page_text + " " + line.get("text", "")

        page_text.strip(" ")
        page_data[page_id] = page_text
    return page_data



def get_np_from_text(page_data):
    np_dict = {}
    for key in page_data.keys():
        page_text = page_data[key]
        page_text_word = nltk.word_tokenize(page_text)
        word_tags = nltk.pos_tag(page_text_word)
        for word_tag in word_tags:
            word, tag = word_tag
            if "NP" in tag:
                np_dict.setdefault(word, [])
                np_dict[word].append(key)

    np_dict = {key: list(set(np_dict[key])) for key in np_dict.keys()}
    return np_dict

def __handle_pdf(request_id, file_path, pdf_id, tenant = "all"):
    logger.info("request-id: {} 's the pdf_id is {}".format(request_id, pdf_id))
    flag = True
    while flag:
        process_dic = get_conversion_status(pdf_id)
        get_redis().set("process:" + request_id, json.dumps(process_dic))
        if process_dic.get("status", "") == "completed":
            logger.info("request-id: {} 's the pdf_id is {}, process is {}".format(request_id, pdf_id, process_dic))
            status = process_dic.get('conversion_status', {}).get("html", {}).get("status", "")
            if status == "completed":
                flag = False
                break
        time.sleep(3)

    lines_data = get_pdf_lines_data(pdf_id)
    page_data = get_page_data(lines_data)
    np_dict = get_np_from_text(page_data)
    get_pdf_html_data(pdf_id)

    page_one = lines_data.get("pages")[0]
    title, author_texts, abstract = get_page_one(page_one)
    authors = get_authors(author_texts)

    file_name = pdf_id + ".html"
    noun_words = doc_flow.get_chunks(pdf_id, page_data, tenant)


    phase_len = 20
    if phase_len >= len(noun_words):
        phase_len = len(noun_words)
    meta = {"title": title, "authors": authors, "abstract": abstract, "phase": noun_words[:phase_len]}

    get_redis().set("meta:" + tenant + ":" + pdf_id, json.dumps(meta))
    client.fput_object('data', file_name, file_name)
    os.remove(file_name)
    file_json = pdf_id + ".json"
    dump_json(file_json, lines_data)
    client.fput_object('data', file_json, file_json)
    logger.info("request-id: {} handle {} pdf end!".format(request_id, pdf_id))
    return


def handle_pdf(request_id, file_path, callback_url):
    pdf_id_dic = process_pdf_by_mathpix(file_path)
    pdf_id = pdf_id_dic.get("pdf_id", None)
    
    if pdf_id is not None:
        thread = threading.Thread(target = __handle_pdf, args = (request_id, file_path, pdf_id, "user"), daemon = True)
        thread.start()

    return pdf_id

def handle_search(request_id, pdf_id, user_text):
    result = doc_flow.search(pdf_id, user_text)
    result["request_id"] = request_id
    return result

# ps aux | grep AIGC |  awk '{print $2}' | xargs kill -9

def handle_batch(request_id, file_paths, tenant = "all"):
    pdf_ids = []
    for path in file_paths:
        pdf_id_dic = process_pdf_by_mathpix(path)
        pdf_id = pdf_id_dic.get("pdf_id", None)
        pdf_ids.append(pdf_id)
        if pdf_id is not None:
            thread = threading.Thread(target = __handle_pdf, args = (request_id, path, pdf_id, tenant), daemon = True)
            thread.start()

    redis = get_redis()
    source_pdf_ids = redis.get("pdfs:" + tenant)
    if source_pdf_ids is None:
        source_pdf_ids = pdf_ids
    else:
        source_pdf_ids = json.loads(source_pdf_ids)
        source_pdf_ids.extend(pdf_ids)

    redis.set("pdfs:" + tenant, json.dumps(source_pdf_ids))
    return pdf_ids


def get_pdf_ids(request_id,tenant = "all"):
    redis = get_redis()
    source_pdf_ids = redis.get("pdfs:" + tenant)
    if source_pdf_ids is None:
        source_pdf_ids = []
    else:
        source_pdf_ids = json.loads(source_pdf_ids)
    all_metas = doc_flow.get_pdf_metas(source_pdf_ids)
    source_pdf_ids = [item + ".html" for item in source_pdf_ids]
    source_pdf_urls = [client.presigned_get_object('data', item) for item in source_pdf_ids]

    for meta in all_metas:
        meta["pdf_id"] = client.presigned_get_object('data', meta['pdf_id'] + ".html")
    result = {"pdfs": source_pdf_urls, "metas": all_metas, "bucket": "data"}
    return result

