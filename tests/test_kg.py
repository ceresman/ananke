# Copyright 2023 undefined
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest,json,os,time
from ananke.data.general  import Paper
from ananke.llm.azure import Azure
from py2neo import Graph, Node, Relationship
from dataclasses import dataclass, asdict
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Collection,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
)

# import sys
# __import__('pysqlite3')
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from ananke.base import BaseObject
from nltk.tokenize import sent_tokenize
from ananke.data import Entity, Relation, Triple
from ananke.data import Chunk, Document,Sentence, Meta
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ananke.db.vector import ChromaStorage

class Neo4jGraph(object):
    def __init__(self, **kwargs):
        self.host = kwargs.get("kg_host")
        self.port = kwargs.get("kg_port")
        self.user = kwargs.get("kg_user")
        self.passwd = kwargs.get("kg_passwd")
        self.db = kwargs.get("kg_db")
        self.graph = py2neo.Graph("neo4j://" + self.host + ":" + self.port, auth = (self.user, self.passwd), name = self.db)

    def update_props(self, entity: Entity) -> dict:
        entity.propertys["label"] = entity.label
        entity.propertys["name"] = entity.name
        return entity.propertys

    def insert(self, triples: List[Triple]):
        for triple in triples:
            sub_label, sub_name = triple.sub.label, triple.sub.name
            obj_label, obj_name = triple.obj.label, triple.obj.name
            sub_props = self.update_props(triple.sub)
            obj_props = self.update_props(triple.obj)
            node_sub = Node(sub_label, **sub_props)
            node_obj = Node(obj_label, **obj_props)
            self.graph.create(node_sub)
            self.graph.create(node_obj)
            realtion = Relationship(node_sub, triple.pred.name, node_obj)
            self.graph.create(realtion)

    def delete(self,):
        pass

    def match(self,):
        pass


# graph = Graph("http://localhost:7474/", auth=("neo4j", "123456"), name='neo4j')
import py2neo
# graph_3 = py2neo.Graph("neo4j://localhost:7687", auth = ("neo4j", "123456"))

kg_dict = {"kg_host": "localhost", "kg_port": "7687", "kg_user": "neo4j", "kg_passwd": "123456", "kg_db": "neo4j"}
kg = Neo4jGraph(**kg_dict)

# sub = Entity("英雄", "张无忌", {"hy": [1111111,  2222222]}, "1024", 1, 1)
# obj = Entity('派别', "明教", {}, "1025", 2, 2)
# pred = Relation("属于", "一种归属描述", 3, "1025", 3)
# triple = Triple(11, "11", sub, pred, obj)

# sub2 = Entity("英雄", "张翠山", {}, "1024", 12, 12)
# obj2 = Entity('派别', "武当山", {}, "1025", 22, 22)
# pred2 = Relation("属于", "一种归属描述", 32, "10252", 32)
# triple2 = Triple(22, "22", sub2, pred2, obj2)

# kg.insert([triple, triple2])

entity_prompt = """Your goal is to build a graph database. Your task is to extract information from a given text content and convert it into a graph database.
Provide a set of Nodes in the form [ENTITY_ID, TYPE, PROPERTIES] and a set of relationships in the form [ENTITY_ID_1, RELATIONSHIP, ENTITY_ID_2, PROPERTIES].
It is important that the ENTITY_ID_1 and ENTITY_ID_2 exists as nodes with a matching ENTITY_ID. If you can't pair a relationship with a pair of nodes don't add it.
When you find a node or relationship you want to add try to create a generic TYPE for it that describes the entity you can also think of it as a label.
Here , I give you an example of the task:

Example Text Input:

```markdown
Data: Alice lawyer and is 25 years old and Bob is her roommate since 2001. Bob works as a journalist. Alice owns a the webpage www.alice.com and Bob owns the webpage www.bob.com.
```

Example Nodes & Relationships Output:
{
    "Nodes": ["alice", "Person", {"age": 25, "occupation": "lawyer", "name":"Alice"}], ["bob", "Person", {"occupation": "journalist", "name": "Bob"}], ["alice.com", "Webpage", {"url": "www.alice.com"}], ["bob.com", "Webpage", {"url": "www.bob.com"}],
    "Relationships": ["alice", "roommate", "bob", {"start": 2021}], ["alice", "owns", "alice.com", {}], ["bob", "owns", "bob.com", {}]
}
OK, here is the end of the task example.
please output with the given example json format. If you understand your mission rules , please handle now.
"""

from uuid import uuid4

def get_uuid():
    _uuid = str(uuid4())
    _uuid = _uuid.split("-")
    _uuid = "".join(_uuid)
    return _uuid

import threading

class AutoIds(object):
    def __init__(self, **kwargs):
        self.doc = {"id": 0, "emb_id": 0, "lock": threading.Lock()}
        self.chunk = {"id": 0, "emb_id": 0, "lock": threading.Lock()}
        self.sent = {"id": 0, "emb_id": 0, "lock": threading.Lock()}
        self.node = {"id": 0, "emb_id": 0, "lock": threading.Lock()}
        self.rel = {"id": 0, "emb_id": 0, "lock": threading.Lock()}
        self.triple = {"id": 0, "emb_id": 0, "lock": threading.Lock()}

        self.names2id = {"doc": self.doc, "chunk": self.chunk, "sent": self.sent,
                        "node": self.node, "rel": self.rel, "triple": self.triple}

    def get_doc_ids(self, length):
        return self.get_ids(length, "doc")

    def get_chunk_ids(self, length):
        return self.get_ids(length, "chunk")

    def get_sent_ids(self, length):
        return self.get_ids(length, "sent")

    def get_node_ids(self, length):
        return self.get_ids(length, "node")

    def get_rel_ids(self, length):
        return self.get_ids(length, "rel")

    def get_triple_ids(self, length):
        return self.get_ids(length, "triple")

    def get_ids(self, length: int, key = "doc"):
        start_id = 0
        item = self.names2id.get(key)
        item.get("lock").acquire()
        start_id =  item["id"]
        item["id"] += length
        item.get("lock").release()

        return start_id

# auto_ids = AutoIds()
# doc_id = auto_ids.get_doc_ids(10)
# print(doc_id)


from ananke.utils.arxiv_dump import process_pdf

class DocFlow(BaseObject):
    def __init__(self, size = 8000, overlap = 256, seps = ["\n\n", "\n", " ", ""], **kwargs):
        super().__init__(**kwargs)
        self.kwargs  = kwargs 
        self.graph = Neo4jGraph(**kwargs)
        self.vector = ChromaStorage(**kwargs)
        self.id_generator = AutoIds(**kwargs)
        self.splitter = RecursiveCharacterTextSplitter(chunk_size = 8000, chunk_overlap = 256, separators = ["\n\n", "\n", " ", ""])
        self.entity_prompt = entity_prompt
        self.vector.create_collection("all-chunk")
        self.vector.create_collection("all-sent")


    def set_splitter(self, size = 8000, overlap = 256, seps = ["\n\n", "\n", " ", ""]):
        self.splitter = RecursiveCharacterTextSplitter(chunk_size = size, chunk_overlap = overlap, separators = seps)


    def get_embedding(self, text) -> (int, List[int]):
        open_ai = Azure(self.kwargs.get("api_key"), self.kwargs.get("api_version"), azure_endpoint = self.kwargs.get("endpoint"))
        embedding = open_ai.embedding(text)
        return embedding


    def set_props(self, props, uid, doc_id, chunk_id, sent_id, emb_id, genre):
        if type(props) == str:
            try:
                props = json.loads(props)
            except Exception:
                props = {}
        elif type(props) == list:
            props = {}

        props["id"] = uid
        props["uuid"] = get_uuid()
        props["doc_id"] = doc_id
        props["chunk_id"] = chunk_id
        props["sent_id"] = sent_id
        props["emb_id"] = emb_id
        props["genre"] = genre

        return props

    def get_entities(self, doc_id, chunk_id, sent_id, nodes):
        entities, names = [], {}
        start_id = self.id_generator.get_node_ids(len(nodes))
        for ix, node in enumerate(nodes, start = start_id):
            name, label, propertys = node[0].lower(), node[1].lower(), node[2]
            if propertys is None:
                propertys = {}
            propertys = self.set_props(propertys, ix, doc_id, chunk_id, sent_id, ix, 1)
            entity = Entity(label, name, propertys)
            names[name] = entity
            entities.append(entity)
        return entities, names


    def __get_triples__(self, doc_id, chunk_id, sent_id, names, relations):
        triples = []
        if relations is None:
            return triples

        start_id = self.id_generator.get_rel_ids(len(relations))
        for rel_id, rel in enumerate(relations, start = start_id):
            if len(rel) != 3:
                continue

            sub, rel_name, obj, props = rel[0], rel[1], rel[2], rel[-1]
            if names.get(sub) is not None and names.get(obj) is not None:
                props = self.set_props(props, rel_id, doc_id, chunk_id, sent_id, rel_id, 0)
                sub = names.get(sub)
                obj = names.get(obj)
                relation = Relation("", rel_name, props)
                triple = Triple(rel_id, get_uuid(), sub, relation, obj)
                triples.append(triple)
            else:
                continue

        return triples

    def get_entity_response(self, text):
        open_ai = Azure(self.kwargs.get("api_key"), self.kwargs.get("api_version"), azure_endpoint = self.kwargs.get("endpoint"))
        # self.logger.info("entity-input:{}".format(self.entity_prompt + text))
        chat_response = open_ai.get_entity(self.entity_prompt + text)
        return chat_response

    def get_sent_summary(self, text):
        return self.get_entity_response(text)

    def get_chunk_summary(self, text):
        return self.get_entity_response(text)

    def get_nodes_and_relation(self, nodes_dict:str):
        nodes, realtion = None, None
        for item in nodes_dict.keys():
            if item.lower() == "nodes":
                nodes = nodes_dict.get(item, None)

            if item.lower() == "relationships":
                realtion = nodes_dict.get(item, None)

        return nodes, realtion

    def get_triples(self, nodes_dict, doc_id, chunk_id, sent_id)->(str, List[Entity], List[Triple]):
        triples = []

        nodes, relations = self.get_nodes_and_relation(nodes_dict)
        nodes = [[item[0].lower(), item[1].lower(), item[-1]] for item in nodes]
        relations = [[item[0].lower(), item[1].lower(), item[2].lower(), item[-1]] for item in relations]
        self.logger.info("triples-nodes:{}".format(nodes))
        self.logger.info("triples-relatins:{}".format(relations))

        entities, names = self.get_entities(doc_id, chunk_id, sent_id, nodes)
        triples  = self.__get_triples__(doc_id, chunk_id, sent_id, names, relations)
        return (entities, triples)        

    def get_docs(self, doc_paths:List[str], tenant = "all")-> List[Document]:
        docs =  []

        start_id = self.id_generator.get_doc_ids(len(doc_paths))
        for ix, item in enumerate(doc_paths, start = start_id):
            data = process_pdf(path)
            doc_uuid = get_uuid()
            meta = Meta(ix, doc_uuid, "", "", {})
            doc = Document(get_uuid(), ix, data, meta, ix)
            docs.append(doc)

        return docs

    def get_chunks(self, docs: List[Document], tenant = "all")->List[Chunk]:
        chunks = []

        for doc in docs:
            doc_chunks = []
            raw_texts = self.splitter.split_text(doc.doc_text)
            chunk_start_id = self.id_generator.get_chunk_ids(len(raw_texts))
            for chunk_id, raw_text in enumerate(raw_texts, start = chunk_start_id):
                chunk_uuid = get_uuid()
                chunk = Chunk(chunk_uuid, chunk_id, raw_text, None, chunk_id, doc.doc_id, None, None)
                doc_chunks.append(chunk)
                chunks.append(chunk)
            doc.chunks = doc_chunks

        return chunks

    def illegal_summary(self, summary: dict)->bool:
        cnt = 0
        nodes = summary.get("Nodes")
        rels = summary.get("Relationships")

        for node in nodes:
            if "alice" in node or "bob" in node:
                cnt += 1
        if cnt:
            return False

        return True
    
    def get_chunks_triples(self, chunks: List[Chunk]):
        chunk_triples = []
        for chunk in chunks:
            summary = self.get_chunk_summary(chunk.chunk_text)
            summary = json.loads(summary)

            if summary is None or len(summary.keys()) == 0 or not self.illegal_summary(summary):
                continue

            _, triples = self.get_triples(summary, chunk.parent_doc_id, chunk.chunk_id, -1)
            chunk.triples = triples
            chunk_triples.extend(triples)

        self.graph.insert(chunk_triples)
        # return triples

    def get_chunks_embeddings(self, chunks:List[Chunk], tenant = "all"):
        ids = []
        metas = []
        embeddings = []
        texts = []

        for chunk in chunks:
            ids.append(chunk.chunk_id)
            texts.append(chunk.chunk_text)
            metas.append({"doc_id": chunk.parent_doc_id, "chunk_id": chunk.chunk_id})
            embeddings.append(self.get_embedding(chunk.chunk_text))

        self.vector.add("all-chunk", embeddings, metas, ids, texts)

    def get_sents(self, chunks: List[Chunk], tenant = "all")->(List[Sentence], List[Chunk]):
        sents = []

        for chunk in chunks:
            chunk_sents = []
            raw_sents = sent_tokenize(chunk.chunk_text)
            start_id  = self.id_generator.get_sent_ids(len(raw_sents))
            for ix, raw_sent in enumerate(raw_sents, start = start_id):
                sent = Sentence(get_uuid(), ix, raw_sent, ix, chunk.chunk_id, chunk.parent_doc_id, None)
                chunk_sents.append(sent)
                sents.append(sent)
            chunk.sents = chunk_sents

        return sents

    def get_sents_embeddings(self, sents:List[Sentence], min_len = 5):
        ids = []
        metas = []
        embeddings = []
        texts = []

        for sent in sents:
            if len(sent.sent_text) <= min_len:
                continue

            metas.append({"doc_id": sent.parent_doc_id, "chunk_id": sent.parent_chunk_id, "sent_id": sent.sent_id})
            ids.append(sent.sent_id)
            embeddings.append(self.get_embedding(sent.sent_text))
            texts.append(sent.sent_text)

        self.vector.add("all-sent", embeddings, metas, ids, texts)

    def get_sents_triples(self, sents:List[Sentence], min_len = 5):
        sent_trples = []
        for sent in sents:
            if len(sent.sent_text) <= min_len:
                continue

            summary = self.get_sent_summary(sent.sent_text)
            summary = json.loads(summary)

            if summary is None or len(summary.keys()) == 0:
                continue

            _, triples = self.get_triples(summary, sent.parent_doc_id, sent.parent_chunk_id, sent.sent_id)
            self.logger.info("triples: {}".format(triples))
            sent.triples = triples
            sent_trples.extend(triples)

        self.graph.insert(sent_trples)

        return sent_trples


    def is_empty_triple(self, entity_and_rel):
        if entity_and_rel is None:
            return True

        if type(entity_and_rel) == list and len(entity_and_rel) == 0:
            return True


        if type(entity_and_rel) == dict and len(entity_and_rel.keys()) == 0:
            return True

        return False


    def search(self, user_text: str, mode = "and"):
        ret = None
        nodes, relations = [], []
        self.logger.info("start to search!")
        user_emb = self.get_embedding(user_text)
        search_chunks = self.vector.query("all-chunk", user_emb, top_n = 50)
        search_sents = self.vector.query("all-sent", user_emb, top_n = 50)

        sent_metas = search_sents.get("metadatas")
        best_meta = sent_metas[0][0]
        best_sent_id, best_chunk_id, best_doc_id = best_meta.get("sent_id"), best_meta.get("chunk_id"), best_meta.get("doc_id")

        chunk_metas = search_chunks.get("metadatas")[0]
        chunk_docs  = search_chunks.get("documents")
        for meta, doc in zip(chunk_metas, chunk_docs):
            if best_chunk_id == meta.get("chunk_id"):
                ret = doc
                break

        entity_and_rel = self.get_chunk_summary(user_text)
        entity_and_rel = json.loads(entity_and_rel)
        if not self.is_empty_triple(entity_and_rel):
            nodes, relations = self.get_nodes_and_relation(entity_and_rel)
            nodes = [[item[0].lower(), item[1].lower(), item[-1]] for item in nodes]
            relations = [[item[0].lower(), item[1].lower(), item[2].lower(), item[-1]] for item in relations]

            self.logger.info("nodes: {}".format(nodes))
            self.logger.info("rels: {}".format(relations))


        if type(ret) == str:
            return ret
        else:
            return ret[0]



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

path = "example/data/gpt3.pdf"

doc_flow = DocFlow(size = 1024, **dic)
docs = doc_flow.get_docs([path])
chunks = doc_flow.get_chunks(docs)
# print(len(chunks))
chunks = chunks[0:16]
# chunks_embs = doc_flow.get_chunks_embeddings(chunks)
sents = doc_flow.get_sents(chunks)
# print(sents)
# print(len(sents))
# sents_embs = doc_flow.get_sents_embeddings(sents[:len(sents) // 2])


# user_text = sents[0].sent_text
# res = doc_flow.search(user_text)
# print(type(res))
# print(type(res))


# doc_flow.get_chunks_triples(chunks)
# doc_flow.get_sents_triples([sents[0]])
# doc_flow.get_sents_triples([sents[0]])


# from ananke.data.math_logic import Agent

# agent = Agent(**dic)


import io
from minio import Minio

client = Minio('ele.ink:19000',access_key='admin_minio',secret_key='admin_minio',secure=False)
url = client.presigned_get_object("data", "gpt3.pdf")

#!/usr/bin/env python
import requests
import json

headers = {
    "app_id": "prismer_eb9b69_0f28c4",
    "app_key": "2796ffd82e527755f9f593ac2091d4bf76036534ca2ca2e39532814f5f75ff00",
    "Content-type": "application/json"
}


def process_pdf_by_mathpix(pdf_url):
    url = "https://api.mathpix.com/v3/pdf"
    headers = {
        "app_id": "prismer_eb9b69_0f28c4",
        "app_key": "2796ffd82e527755f9f593ac2091d4bf76036534ca2ca2e39532814f5f75ff00",
        "Content-type": "application/json"
    }

    data = {
        "url": pdf_url,
        "conversion_formats": {
            "docx": True,
            "tex.zip": True,
            "html": True
        }
    }

    print(data)
    req = requests.post(url, json = data, headers = headers)
    return json.loads(req.content)

def get_process_status(pdf_id):
    url = "https://api.mathpix.com/v3/pdf/{}".format(pdf_id)
    req = requests.get(url, headers = headers)
    return json.loads(req.content)

def get_conversion_status(pdf_id):
    url = "https://api.mathpix.com/v3/converter/{}".format(pdf_id)
    req = requests.get(url, headers = headers)
    return json.loads(req.content)

# url = "http://cs229.stanford.edu/notes2020spring/cs229-notes1.pdf"
# req_dict = process_pdf_by_mathpix(url)
# pdf_id = req_dict.get("pdf_id")
pdf_id = "2024_03_24_cfc7ecd05c02d28a9158g"
# status = get_process_status(pdf_id)
# print(url)
# print(pdf_id)
# print(status)

# status = get_conversion_status(pdf_id)
# print(status)

def get_pdf_html_data(pdf_id):
    url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".html"
    response = requests.get(url, headers=headers)
    # with open(pdf_id + ".html", "wb") as f:
    #     f.write(response.content)
    return (response.content)

def get_pdf_lines_data(pdf_id):
    url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".lines.json"
    response = requests.get(url, headers = headers)
    with open(pdf_id + ".lines.json", "w") as f:
        json.dump(json.loads(response.content), f, indent = 4)
    return json.loads(response.content)
    # with open(pdf_id + ".lines.json", "w") as f:
    #     f.write(response.text)

lines_data = get_pdf_lines_data(pdf_id)


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

page_data = get_page_data(lines_data)
print(page_data[1])

import nltk

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


np_dict = get_np_from_text(page_data)
# print(np_dict)