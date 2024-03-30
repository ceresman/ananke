import requests, json

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


lines_data = get_pdf_lines_data(pdf_id)
# print(page_data)

page1 = lines_data.get("pages")[0]
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

title, author_texts, abstract = get_page_one(page1)
authors = get_authors(author_texts)

meta = {"title": title, "authors": authors, "abstract": abstract}
print(meta)