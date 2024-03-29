import json, requests


headers = {
    "app_id": "prismer_eb9b69_0f28c4",
    "app_key": "2796ffd82e527755f9f593ac2091d4bf76036534ca2ca2e39532814f5f75ff00",
    "Content-type": "application/json"
}

pdf_id = "2024_03_25_9ee7aaffb8211eb2dfc7g"
def get_pdf_lines_data(pdf_id):
    url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".lines.json"
    response = requests.get(url, headers = headers)
    with open(pdf_id + ".lines.json", "w") as f:
        json.dump(json.loads(response.content), f, indent = 4)

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

lines_data = get_pdf_lines_data(pdf_id)
page_data = get_page_data(lines_data)
