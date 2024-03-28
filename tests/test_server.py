import io, requests,json    
from minio import Minio

client = Minio('ele.ink:19000',access_key='admin_minio',secret_key='admin_minio',secure=False)
gpt3_url = client.presigned_get_object("data", "gpt3.pdf")

file_url = "http://cs229.stanford.edu/notes2020spring/cs229-notes1.pdf"
file_type = "pdf"
request_id = "willamhou-doc"

data = {
    "request_id": request_id,
    "file_path": file_url,
    "file_type": file_type,
    "callback_url": "http://127.0.0.1:18080/aigc/query",
}


# url = "http://127.0.0.1:18080/aigc/upload_doc"
# # url = "http://ele.ink:18080/aigc/upload_doc"
# # req = requests.post(url, data = json.dumps(data))
# req = requests.post(url, json = (data))
# print(req.content)


data = {"request_id": "hhhhhhh", "text": "logic", "search_type": "logic"}

# url = "http://127.0.0.1:18080/aigc/search"
# req = requests.post(url, json = data)
# print(req.content, req.status_code)


headers = {
    "app_id": "prismer_eb9b69_0f28c4",
    "app_key": "2796ffd82e527755f9f593ac2091d4bf76036534ca2ca2e39532814f5f75ff00",
    "Content-type": "application/json"
}



pdf_id = "2024_03_25_9ee7aaffb8211eb2dfc7g"
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


# lines_data = get_pdf_lines_data(pdf_id)
# page_data = get_page_data(lines_data)
# print(page_data)

data = {
    "request_id": request_id,
    "file_path": file_url,
    "file_type": file_type,
    # "callback_url": "http://127.0.0.1:18080/aigc/query",
}

# url = "http://127.0.0.1:18080/aigc/upload_doc"
# url = "http://ele.ink:18080/aigc/upload_doc"
# req = requests.post(url, data = json.dumps(data))
# req = requests.post(url, json = (data))
# print(req.content)
# print(json.loads(req.content))


url = "http://127.0.0.1:18080/aigc/search"

data = {
    "request_id" : "willamhou-search",
    "pdf_id": "2024_03_28_d918ce007641daed7730g",
    "text": "machine learning"
}

req = requests.get(url, params = data)
print(req.content)