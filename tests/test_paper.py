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