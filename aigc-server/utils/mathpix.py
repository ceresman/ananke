#! /usr/bin/python
#-*- coding:utf-8 -*-
import requests, json
import threading, time
import nltk
from utils.log import logger

headers = {
    "app_id": "prismer_eb9b69_0f28c4",
    "app_key": "2796ffd82e527755f9f593ac2091d4bf76036534ca2ca2e39532814f5f75ff00",
    "Content-type": "application/json"
}


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
    req = requests.post(url, json = data, headers = headers)
    try:
        return json.loads(req.content)
    except Exception as err:
        logger.info("process_pdf_error:code {}, msg: {}".format(req.status_code, req.content))
        return {}


def get_process_status(pdf_id):
    url = "https://api.mathpix.com/v3/pdf/{}".format(pdf_id)
    req = requests.get(url, headers = headers)
    return json.loads(req.content)

def get_conversion_status(pdf_id):
    url = "https://api.mathpix.com/v3/converter/{}".format(pdf_id)
    req = requests.get(url, headers = headers)
    return json.loads(req.content)



def get_pdf_html_data(pdf_id):
    url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".html"
    response = requests.get(url, headers=headers)
    with open(pdf_id + ".html", "wb") as f:
        f.write(response.content)

    return (response.content)

def get_pdf_lines_data(pdf_id):
    url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".lines.json"
    response = requests.get(url, headers = headers)
    # with open(pdf_id + ".lines.json", "w") as f:
    #     json.dump(json.loads(response.content), f, indent = 4)

    return json.loads(response.content)

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

def __handle_pdf(request_id, file_path, callback_url):
    pdf_id_dic = process_pdf_by_mathpix(file_path)
    pdf_id = pdf_id_dic.get("pdf_id", None)

    if pdf_id is None:
        data = {"request_id" : request_id, "msg": "pdf hanlde error!"}
        requests.post(callback_url, json = data)
        return

    logger.info("request-id: {} 's the pdf_id is {}".format(request_id, pdf_id))
    for i in range(0, 1000):
        process_dic = get_process_status(pdf_id)
        if process_dic.get("status", "") == "completed":
            break
        time.sleep(3)

    lines_data = get_pdf_lines_data(pdf_id)
    html_data = get_pdf_html_data(pdf_id)
    page_data = get_page_data(lines_data)
    np_dict = get_np_from_text(page_data)

    data = {
        "request_id": request_id,
        "pages" : lines_data.get("pages", []),
        "html": html_data,
        "np_dict": np_dict 
    }

    req = requests.post(callback_url, json = data)
    logger.info("callback_url-{}, status: {}".format(callback_url, req.status_code))
    return


def handle_pdf(request_id, file_path, callback_url):
    thread = threading.Thread(target = __handle_pdf, args = (request_id, file_path, callback_url), daemon = True)
    thread.start()


__handle_pdf("11111", "http://cs229.stanford.edu/notes2020spring/cs229-notes1.pdf", "")
# ps aux | grep AIGC |  awk '{print $2}' | xargs kill -9