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
    descriptions: List[str]
    entity_uuid: str
    entity_id: int
    entity_emb_id: int

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
    triples: List[Triple]

@dataclass
class Chunk:
    chunk_uuid: str
    chunk_id : int
    chunk_text: str
    chunk_summary: str
    chunk_emb_id: int
    parent_doc_id: int
    sents: List[Sentence]
    triples: List[Triple]

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

class MySQL(object):
    def __init__(self, **kwargs):
        self.host = kwargs.get("msyql_host")
        self.user = kwargs.get("mysql_user")
        self.passwd = kwargs.get("msyql_password")
        self.db_name = kwargs.get("mysql_dbname")
        self.conn = pymysql.connect(host = self.host, user = self.user, passwd = self.passwd,
                    port = 3306, database = self.db_name, charset='utf8')
        self.batch = 2

    def insert_data(self, sql, data):
        cursor = self.conn.cursor()
        cursor.executemany(sql, data)
        self.conn.commit()
        auto_incre_id = cursor.lastrowid
        cursor.close()
        return auto_incre_id;

    def insert_document(self, tenant, docs: List[Document]):
        sql = "insert into documents(tenant, doc_uuid, doc_text, doc_emb_id, doc_meta_id) values(%s,%s,%s,%s,%s);"
        times, remain = len(docs)//self.batch, len(docs)%self.batch

        for i in range(times):
            data = []
            auto_incre_id = -1
            batches = docs[i * self.batch : (i + 1) * self.batch]
            for item in batches:
                insert = (tenant, item.doc_uuid, item.doc_text, item.doc_emb_id, item.doc_meta.meta_id)
                data.append(insert)

            auto_incre_id = self.insert_data(sql, data)
            for ix in range(i * self.batch, (i + 1) * self.batch):
                docs[ix].doc_id = auto_incre_id
                auto_incre_id += 1

        if remain != 0:        
            data = []
            batches = docs[times * self.batch:]
            for item in batches:
                insert = (tenant, item.doc_uuid, item.doc_text, item.doc_emb_id, item.doc_meta.meta_id)
                data.append(insert)

            auto_incre_id = self.insert_data(sql, data)
            for ix in range(times * self.batch, len(docs)):
                docs[ix].doc_id = auto_incre_id
                auto_incre_id += 1

        return docs;

    def update_document(self, docs: List[Document]):

        return

    def delete_document(self, docs: List[Document]):
        data = []
        sql = "delete from documents where id in %s;"
        for item in docs:
            data.append(item.doc_id)
        print(data)
        cursor = self.conn.cursor()
        cursor.execute(sql, [data])
        self.conn.commit()
        cursor.close()

    def insert_chunks(self, tenant, chunks: List[Chunk]):
        sql = "insert into chunks(tenant, chunk_uuid, chunk_text, chunk_summary, chunk_emb_id, parent_doc_id) values(%s,%s,%s,%s,%s,%s);"
        times, remain = len(chunks)//self.batch, len(chunks)%self.batch
       
        for i in range(times):
            data = []
            auto_incre_id = -1
            batches = chunks[i * self.batch : (i + 1) * self.batch]
            for item in batches:
                insert = (tenant, item.chunk_uuid, item.chunk_text, item.chunk_summary, item.chunk_emb_id, item.parent_doc_id)
                data.append(insert)

            auto_incre_id = self.insert_data(sql, data)
            for ix in range(i * self.bach, (i + 1) * self.batch):
                chunks[ix].chunk_id = auto_incre_id
                auto_incre_id += 1


        data = []
        auto_incre_id = -1
        batches = chunks[times * self.batch:]
        for item in batches:
            insert = (tenant, item.chunk_uuid, item.chunk_text, item.chunk_summary, item.chunk_emb_id, item.parent_doc_id)
            data.append(insert)
        
        auto_incre_id = self.insert_data(sql, data)
        for ix in range(times * self.batch, len(chunks)):
            chunks[ix].chunk_id = auto_incre_id
            auto_incre_id += 1

        return chunks;


    def update_chunks(self, chunks: List[Chunk]):
        return


    def delete_chunks(self, chunks: List[Chunk]):
        data = []
        sql = "delete from chunks where id in %s;"
        for item in docs:
            data.append(item.chunk_id)

        cursor = self.conn.cursor()
        cursor.execute(sql, tuple(data))
        self.conn.commit()
        cursor.close()


    def insert_sents(self, sents: List[Sentence]):
        sql = "insert into sents(tenant, sent_uuid, sent_text, sent_emb_id, parent_chunk_id, parent_doc_id) values(%s,%s,%s,%s,%s, %s);"
        times, remain = len(sents)//self.batch, len(sents)%self.batch
        
        for i in range(times):
            data = []
            batches = sents[i * self.batch : (i + 1) * self.batch]
            auto_incre_id = -1
            for item in batches:
                insert = (tenant, item.sent_uuid, item.sent_text, item.sent_emb_id, item.parent_chunk_id, item.parent_doc_id)
                data.append(insert)

            auto_incre_id = self.insert_data(sql, data)
            if auto_incre_id != -1:
                for ix in range(i * self.bach, (i + 1) * self.batch):
                    sent[ix].sent_id = auto_incre_id
                    auto_incre_id += 1

        data = []
        auto_incre_id = -1
        batches = sent[times * self.batch:]
        for item in batches:
            insert = (tenant, item.sent_uuid, item.sent_text, item.sent_emb_id, item.parent_chunk_id, item.parent_doc_id)
            data.append(insert)
        
        auto_incre_id = self.insert_data(sql, data)
        if auto_incre_id != -1:
            for ix in range((i + 1) * self.batch, len(sents)):
                sents[ix].sent_id = auto_incre_id
                auto_incre_id += 1

        return sent;


    def update_sents(self, sents: List[Sentence]):
        return

    def delete_sents(self, sents: List[Sentence]):
        data = []
        sql = "delete from sents where id in %s;"
        for item in docs:
            data.append(item.sent_id)

        cursor = self.conn.cursor()
        cursor.execute(sql, [data])
        self.conn.commit()
        cursor.close()


    def insert_triples(self, triples: List[Triple]):
        return

    def update_triples(self, triples: List[Triple]):
        return

    def delete_triples(self, triples: List[Triple]):
        data = []
        sql = "delete from triples where id in %s;"
        for item in docs:
            data.append(item.triple_id)

        cursor = self.conn.cursor()
        cursor.execute(sql, [data])
        self.conn.commit()
        cursor.close()

        return

    def create_tables(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.close()

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
# embs = ernie_model.embedding(model, texts[0:16])
# assert(len(ems) == len(texts))

# sql = "create table documents(id BIGINT AUTO_INCREMENT, tenant varchar(36), doc_uuid varchar(36), doc_text LONGTEXT, doc_emb_id BIGINT, doc_meta_id BIGINT, PRIMARY KEY  (`id`)) ENGINE=InnoDB character set utf8;"

mysql = MySQL(msyql_host = "localhost", mysql_user = "root", msyql_password = "123456", mysql_dbname = "anake")

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
# docs = mysql.insert_document("houyu", docs)

# # print("doc_1 - {}".format(doc.doc_id))
# # print(doc2.doc_id)
# for item in docs:
#     print(item.doc_id)

mysql.delete_document(docs)