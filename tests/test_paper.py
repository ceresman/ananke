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
import pytest
from ananke.data.general  import Paper

__author__ = "OOXXXXOO"
__copyright__ = "OOXXXXOO"
__license__ = "MIT"

# def test_paper():
#     path = "example/data/gpt3.pdf"
#     # config = YAMLCONFIG()
#     paper = Paper()
#     data = paper.read(path)
#     return data

from ananke.utils.arxiv_dump import process_pdf

from uuid import uuid4

def get_uuid():
    _uuid = str(uuid4())
    _uuid = _uuid.split("-")
    _uuid = "".join(_uuid)
    return _uuid


# print(get_uuid())

import nltk
import pymysql
from nltk.tokenize import sent_tokenize
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ananke.base import BaseDocument, BaseChunk, BaseSentence
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


@dataclass
class Entity:
    label: str
    name: str
    propertys: dict
    entity_uuid: str
    entity_id: int
    entity_emb_id: int
    descriptions: List[str] = None

@dataclass
class Relation:
    name: str
    description: str
    relation_id: int
    relation_uuid: str
    relation_emb_id: int

@dataclass
class Triple:
    triple_id: int
    triple_uuid: str
    sub: Entity
    pred: Relation
    obj: Entity

@dataclass
class Sentence:
    sent_uuid: str
    sent_id: int
    sent_text: str
    sent_emb_id: int
    parent_chunk_id: int 
    parent_doc_id: int
    triples: List[Triple] = None

@dataclass
class Chunk:
    chunk_uuid: str
    chunk_id : int
    chunk_text: str
    chunk_summary: str
    chunk_emb_id: int
    parent_doc_id: int
    sents: List[Sentence] = None
    triples: List[Triple] = None

@dataclass
class Meta:
    meta_uuid: str
    meta_id: int
    meta_type: str
    meta_value: dict
    meta_json: str

@dataclass
class Document:
    doc_uuid: str
    doc_id : int
    doc_text: str
    doc_meta: Meta
    doc_emb_id: int
    chunks: List[Chunk] = None

def get_sentence(chunk):
    sents = []
    raw_sents = sent_tokenize(chunk.chunk_text)
    for item in raw_sents:
        sent = Sentence(sent_uuid = get_uuid(), sent_text = item,
                    parent_doc_id = chunk.parent_doc_id,
                    parent_chunk_id = chunk.chunk_id,
                    sent_id = None, sent_emb_id = None, triples = None)
        sents.append(sent)
    return sents

def get_chunks(docs:List[Document], start_id = 0, size = 8000, overlap = 256, seps = ["\n\n", "\n", " ", ""]):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = size, chunk_overlap = overlap, separators = seps)
    chunks, sents = [], []
    for doc in docs:
        chunk_texts = text_splitter.split_text(doc.doc_text)
        for chunk_text in chunk_texts:
            chunk = Chunk(chunk_text = chunk_text, chunk_id = 0, 
                        chunk_uuid = get_uuid(), sents = None, 
                        parent_doc_id = doc.doc_id, chunk_summary = None, 
                        chunk_emb_id = None, triples = None)
            chunk.sents = get_sentence(chunk)
            chunks.append(chunk)
            sents.extend(chunk.sents)
    return chunks, sents


import py2neo
from py2neo import Graph, Node, Relationship, NodeMatch

class Graph(object):
    def __init__(self, **kwargs):
        self.host = kwargs.get("neo4j_host")
        self.user = kwargs.get("neo4j_user")
        self.passwd = kwargs.get("neo4j_passwd")
        self.db = kwargs.get("neo4j_db")
        self.graph = py2neo.Graph(host = host, auth = (self.user, self.passwd), name = self.db)

    def insert(self, triples: List[Triple]):
        for triple in triples:
            sub_label, sub_name = triple.sub.label, triple.sub.name
            obj_label, obj_name = triple.obj.label, triple.obj.name
            node_sub = Node(sub_label, name = sub_name)
            node_obj = Node(obj_label, name = obj_name)

            self.graph.create(node_sub)
            self.graph.create(node_obj)
            node_sub.update(triple.sub.propertys)
            node_obj.update(triple.obj.propertys)
            self.graph.push(node_sub)
            self.graph.push(node_obj)

            realtion = Relationship(node_sub, triple.pred.name, node_obj)
            self.graph.create(realtion)

    def delete(self,):
        pass

    def match(self,):
        pass


# class Meta:
#     meta_id: int
#     meta_uuid: str
#     meta_type: str
#     meta_value: dict
#     meta_json: str

# nltk.download('punkt')
path = "example/data/gpt3.pdf"
data = process_pdf(path)
meta = Meta(1, "", "" , None, "")
doc = Document(get_uuid(), 1, data, meta, 1)
# doc.text = data
# doc.doc_uuid = get_uuid()
chunks, sents = get_chunks([doc])
print(len(get_sentence(chunks[0])))



import erniebot

class ErnieModel(object):
    def __init__(self, api_type='aistudio', access_token=None):
        super(ErnieModel, self).__init__()
        erniebot.api_type = api_type
        erniebot.access_token = access_token

    def chat(self, model, messages):
        response = erniebot.ChatCompletion.create(model=model, messages=messages)
        return response.get_result()

    def embedding(self, model, input_text):
        response = erniebot.Embedding.create(model=model, input=input_text)
        return response.get_result()

# ERNIE:
#   ERNIE4:
#     - API_KEY : d0a03a377c528fdde7775b089298e31a218b8708
#     - MODEL : "ernie-bot-4"
#     - API_TYPE : "aistudio"

token = "d0a03a377c528fdde7775b089298e31a218b8708"
ernie_model = ErnieModel(access_token = token)

model = "ernie-text-embedding"
input_text = ["hhhhhhhhh", "我今天非常高兴"]
# embedding = ernie_model.embedding(model, input_text)
# print(embedding)


texts = []
for sent in sents:
    texts.append(sent.sent_text)

# print(len(texts))
embs = ernie_model.embedding(model, texts[0:16])
# assert(len(ems) == len(texts))

# sql = "create table documents(id BIGINT AUTO_INCREMENT, tenant varchar(36), doc_uuid varchar(36), doc_text LONGTEXT, doc_emb_id BIGINT, doc_meta_id BIGINT, PRIMARY KEY  (`id`)) ENGINE=InnoDB character set utf8;"


# mysql.create_tables(sql)

import copy
doc2 = copy.deepcopy(doc)
doc3 = copy.deepcopy(doc)

doc.doc_meta.meta_id = 1
doc2.doc_meta.meta_id = 2
doc3.doc_meta.meta_id = 3

doc.doc_emb_id = 1
doc2.doc_emb_id = 2
doc3.doc_emb_id = 3

doc.doc_id = 60
doc2.doc_id = 61
doc3.doc_id = 62
docs = [doc, doc2, doc3]
# mysql = MySQL(msyql_host = "localhost", mysql_user = "root", msyql_password = "123456", mysql_dbname = "anake")
# mysql.create_tables(sql)

# docs = mysql.insert_document("houyu", docs)

# # print("doc_1 - {}".format(doc.doc_id))
# # print(doc2.doc_id)
# for item in docs:
#     print(item.doc_id)

# mysql.delete_document(docs)

# print(len(embs))
# print([str(i) for i in range(len(embs))])
# # print(texts[0])
# vector_db = ChromaStorage()
# vector_db.delete_collection("houyu")
# vector_db.create_collection("houyu")
# vector_db.add("houyu", embs, [], [str(i) for i in range(len(embs))], texts[0:16])
# search_result = vector_db.query("houyu", embs[0], top_n = 2)
# print(search_result)

prompt = """
Your goal is to build a graph database. Your task is to extract information from a given text content and convert it into a graph database.
Provide a set of Nodes in the form [ENTITY_ID, TYPE, PROPERTIES] and a set of relationships in the form [ENTITY_ID_1, RELATIONSHIP, ENTITY_ID_2, PROPERTIES].
It is important that the ENTITY_ID_1 and ENTITY_ID_2 exists as nodes with a matching ENTITY_ID. If you can't pair a relationship with a pair of nodes don't add it.
When you find a node or relationship you want to add try to create a generic TYPE for it that describes the entity you can also think of it as a label.
Here , I give you an example of the task:

Example Text Input:

```markdown
Data: Alice lawyer and is 25 years old and Bob is her roommate since 2001. Bob works as a journalist. Alice owns a the webpage www.alice.com and Bob owns the webpage www.bob.com.
```

Example Nodes & Relationships Output:

Nodes: 
```json
["alice", "Person", {"age": 25, "occupation": "lawyer", "name":"Alice"}], ["bob", "Person", {"occupation": "journalist", "name": "Bob"}], ["alice.com", "Webpage", {"url": "www.alice.com"}], ["bob.com", "Webpage", {"url": "www.bob.com"}]
```
Relationships: 
```json
["alice", "roommate", "bob", {"start": 2021}], ["alice", "owns", "alice.com", {}], ["bob", "owns", "bob.com", {}] 
```
OK, here is the end of the task example.
please output with the given example format. If you understand your mission rules , tell me you are ready."""

content = """
The below text is you need to process
```markdown
The National Aeronautics and Space Administration (NASA /ˈnæsə/) is an independent agency of the U.S. federal government responsible for the civil space program, aeronautics research, and space research. Established in 1958, NASA succeeded the National Advisory Committee for Aeronautics (NACA) to give the U.S. space development effort a distinctly civilian orientation, emphasizing peaceful applications in space science.([4])([5])([6]) NASA has since led most American space exploration, including Project Mercury, Project Gemini, the 1968–1972 Apollo Moon landing missions, the Skylab space station, and the Space Shuttle. NASA currently supports the International Space Station and oversees the development of the Orion spacecraft and the Space Launch System for the crewed lunar Artemis program, the Commercial Crew spacecraft, and the planned Lunar Gateway space station.
NASA's science is focused on: better understanding Earth through the Earth Observing System;([7]) advancing heliophysics through the efforts of the Science Mission Directorate's Heliophysics Research Program;([8]) exploring bodies throughout the Solar System with advanced robotic spacecraft such as New Horizons and planetary rovers such as Perseverance;([9]) and researching astrophysics topics, such as the Big Bang, through the James Webb Space Telescope, and the Great Observatories and associated programs.([10]) NASA's Launch Services Program provides oversight of launch operations and countdown management for its uncrewed launches.
```"""

messages = [{"role": "user", "content": prompt + content}]
model = "ernie-3.5"

entities = ernie_model.chat(model, messages)
print(entities)