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

path = "example/data/gpt3.pdf"

data = process_pdf(path)


from uuid import uuid4

def get_uuid():
    _uuid = str(uuid4())
    _uuid = _uuid.split("-")
    _uuid = "".join(_uuid)
    return _uuid


# print(get_uuid())

from langchain.text_splitter import RecursiveCharacterTextSplitter
from nltk.tokenize import sent_tokenize
from ananke.base import BaseDocument, BaseChunk, BaseSentence
import nltk

def get_sentence(chunk):
    sentences = []
    source_sentences = sent_tokenize(chunk)
    for item in source_sentences:
        sentence = BaseSentence()
        sentence.sentece_id = get_uuid()
        sentence.sentence_text = item
        sentences.append(sentence)
    return sentences

def get_chunk_sentences(chunks):

    for chunk in chunks:
        chunk_uuid = get_uuid()
        sentence = get_sentence(chunk)
        sentence_uuid = get_uuid()
    return []

def get_chunks(docs, start_id = 0, size = 8000, overlap = 256, seps = ["\n\n", "\n", " ", ""]):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = size, chunk_overlap = overlap, separators = seps)
    chunks, sentences = [], []
    for doc in docs:
        doc_uuid = get_uuid()
        chunks = text_splitter.split_text(doc)
        # sentences = get_chunk_sentences(chunks)

    return chunks, sentences


chunks, sentences = get_chunks([data])
print(len(get_sentence(chunks[0])))



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

import mysql.connector
import pymysql



@dataclass
class Entity:
    label: str
    name: str
    propertys: dict
    descriptions: List[str]
    entity_uuid: str
    entity_id: long
    entity_emb_id: long

@dataclass
class Relation:
    name: str
    description: str
    relation_id: long
    relation_uuid: str
    relation_emb_id: long

@dataclass
class Triple:
    triple_id: long
    triple_uuid: str
    sub: Entity
    pred: Relation
    obj: Entity

@dataclass
class Sentence:
    sent_uuid: str
    sent_id: long
    sent_text: str
    sent_emb_id: long
    parent_chunk_id: long 
    parent_doc_id: long
    triples: List[Triple]

@dataclass
class Chunk:
    chunk_uuid: str
    chunk_id : long
    chunk_text: str
    chunk_summary: str
    chunk_emb_id: long
    parent_doc_id: long
    sents: List[Sentence]
    triples: List[Triple]

@dataclass
class Meta:
    meta_uuid: str
    meta_id: long
    meta_type: str
    meta_value: dict
    meta_json: str

@dataclass
class Document:
    doc_uuid: str
    doc_id : long
    doc_text: str
    doc_meta: meta
    doc_emb_id: long



class MySQL(object):
    def __init__(self, **kwargs):
        self.host = kwargs.get("msyql_host")
        self.user = kwargs.get("mysql_user")
        self.passwd = kwargs.get("msyql_password")
        self.db_name = kwargs.get("mysql_dbname")
        self.conn = pymysql.connect(host = self.host, user = self.user, passwd = self.passwd, database = self.db_name, charset='utf8')
        self.batch = 128

    def insert_data(self, sql, data):
        cursor = self.conn.cursor()
        cursor.executemany(sql, data)
        self.conn.commit()
        auto_incre_id = cursor.lastrowid
        cursor.close()
        return auto_incre_id;

    def insert_document(self, tenant, docs: List[Document]):
        sql = "insert into documents(tenant, doc_uuid, doc_text, doc_emb_id, doc_meta_id) values(%s,%s,%s,%s,%s);"
        times, remain = len(docs)/self.batch, len(docs)%self.batch
        
        for i in range(times):
            data = []
            batch_data = docs[i * self.batch : (i + 1) * self.batch]
            auto_incre_id = -1
            for item in batches:
                insert = (tenant, item.doc_uuid, item.doc_text, item.doc_meta.meta_id, item.doc_emb_id)
                data.append(insert)
                auto_incre_id = self.insert_data(sql, data)

            if auto_incre_id != -1:
                for ix in range(i * self.bach, (i + 1) * self.batch):
                    docs[i].doc_id = auto_incre_id
                    auto_incre_id += 1


        batches = docs[(i + 1) * self.batch:]
        auto_incre_id = -1
        for item in batches:
            insert = (tenant, item.doc_uuid, item.doc_text, item.doc_meta.meta_id, item.doc_emb_id)
            data.append(insert)
            auto_incre_id = self.insert_data(sql, data)

        if auto_incre_id != -1:
            for ix in range((i + 1) * self.batch, len(docs)):
                docs[i].doc_id = auto_incre_id
                auto_incre_id += 1

        return docs;

    def update_document(self, docs: List[Document]):

        return

    def delete_document(self, docs: List[Document]):
        data = []
        sql = "delete from documents where id in %s;"
        for item in docs:
            data.append(item.doc_id)

        cursor = self.conn.cursor()
        cursor.execute(sql, tuple(data))
        self.conn.commit()
        cursor.close()

    def insert_chunks(self, tenant, chunks: List[Chunk]):
        sql = "insert into chunks(tenant, chunk_uuid, chunk_text, chunk_summary, chunk_emb_id, parent_doc_id) values(%s,%s,%s,%s,%s,%s);"
        times, remain = len(chunks)/self.batch, len(chunks)%self.batch
        
        for i in range(times):
            data = []
            batch_data = chunks[i * self.batch : (i + 1) * self.batch]
            auto_incre_id = -1
            for item in batches:
                insert = (tenant, item.chunk_uuid, item.chunk_text, item.chunk_summary, item.chunk_emb_id, item.parent_doc_id)
                data.append(insert)
                auto_incre_id = self.insert_data(sql, data)

            if auto_incre_id != -1:
                for ix in range(i * self.bach, (i + 1) * self.batch):
                    chunks[i].chunk_id = auto_incre_id
                    auto_incre_id += 1


        batches = chunks[(i + 1) * self.batch:]
        auto_incre_id = -1
        for item in batches:
            insert = (tenant, item.chunk_uuid, item.chunk_text, item.chunk_summary, item.chunk_emb_id, item.parent_doc_id)
            data.append(insert)
            auto_incre_id = self.insert_data(sql, data)

        if auto_incre_id != -1:
            for ix in range((i + 1) * self.batch, len(chunks)):
                chunks[i].chunk_id = auto_incre_id
                auto_incre_id += 1

        return chunks;


    def update_chunks(self, chunks: List[Chunk]):
        return


    def delete_chunks(self, chunks: List[Chunks]):
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
        times, remain = len(sents)/self.batch, len(sents)%self.batch
        
        for i in range(times):
            data = []
            batch_data = sents[i * self.batch : (i + 1) * self.batch]
            auto_incre_id = -1
            for item in batches:
                insert = (tenant, item.sent_uuid, item.sent_text, item.sent_emb_id, item.parent_chunk_id, item.parent_doc_id)
                data.append(insert)
                auto_incre_id = self.insert_data(sql, data)

            if auto_incre_id != -1:
                for ix in range(i * self.bach, (i + 1) * self.batch):
                    sent[i].sent_id = auto_incre_id
                    auto_incre_id += 1


        batches = sent[(i + 1) * self.batch:]
        auto_incre_id = -1
        for item in batches:
            insert = (tenant, item.sent_uuid, item.sent_text, item.sent_emb_id, item.parent_chunk_id, item.parent_doc_id)
            data.append(insert)
            auto_incre_id = self.insert_data(sql, data)

        if auto_incre_id != -1:
            for ix in range((i + 1) * self.batch, len(sents)):
                sents[i].sent_id = auto_incre_id
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
        cursor.execute(sql, tuple(data))
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
        cursor.execute(sql, tuple(data))
        self.conn.commit()
        cursor.close()

        return


import py2neo
from py2neo import Graph, Node, Relationship, NodeMatche

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
