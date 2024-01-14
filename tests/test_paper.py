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



from dataclasses import dataclass
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
class Triple:
    triple_id: long
    triple_uuid: str
    subject_name: str
    subject_desc: str
    pred_name: str
    pred_desc: str
    object_name: str
    object_desc: str


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
        self.db = kwargs.get("mysql_dbname")
        self.connect = pymysql.connect(host = self.host, user = self.user, passwd = self.passwd, database = self.db)
    
    def insert_document(self, docs: List[Document]):

        return

    def update_document(self, docs: List[Document]):

        return

    def delete_document(self, docs: List[Document]):
        return


    def insert_chunks(self, chunks: List[Chunk]):
        return

    def update_chunks(self, chunks: List[Chunk]):
        return


    def delete_chunks(self, chunks: List[Chunks]):
        return

    def insert_sents(self, sents: List[Sentence]):
        return

    def update_sents(self, sents: List[Sentence]):
        return

    def delete_sents(self, sents: List[Sentence]):
        return

    def insert_triples(self, triples: List[Triple]):
        return

    def update_triples(self, triples: List[Triple]):
        return

    def delete_triples(self, triples: List[Triple]):
        return


import py2neo

class Graph(object):
    def __init__(self, **kwargs):
        self.host = kwargs.get("neo4j_host")
        self.user = kwargs.get("neo4j_user")
        self.passwd = kwargs.get("neo4j_passwd")
        self.graph = py2neo.Graph(host = host, auth = (self.user, self.passwd))

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="123456",
#   database="runoob_db"
# )
# mycursor = mydb.cursor()
 
# mycursor.execute("CREATE TABLE sites (name VARCHAR(255), url VARCHAR(255))")