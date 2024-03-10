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

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

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

content = """
The below text is you need to process
```markdown
The National Aeronautics and Space Administration (NASA /ˈnæsə/) is an independent agency of the U.S. federal government responsible for the civil space program, aeronautics research, and space research. Established in 1958, NASA succeeded the National Advisory Committee for Aeronautics (NACA) to give the U.S. space development effort a distinctly civilian orientation, emphasizing peaceful applications in space science.([4])([5])([6]) NASA has since led most American space exploration, including Project Mercury, Project Gemini, the 1968–1972 Apollo Moon landing missions, the Skylab space station, and the Space Shuttle. NASA currently supports the International Space Station and oversees the development of the Orion spacecraft and the Space Launch System for the crewed lunar Artemis program, the Commercial Crew spacecraft, and the planned Lunar Gateway space station.
NASA's science is focused on: better understanding Earth through the Earth Observing System;([7]) advancing heliophysics through the efforts of the Science Mission Directorate's Heliophysics Research Program;([8]) exploring bodies throughout the Solar System with advanced robotic spacecraft such as New Horizons and planetary rovers such as Perseverance;([9]) and researching astrophysics topics, such as the Big Bang, through the James Webb Space Telescope, and the Great Observatories and associated programs.([10]) NASA's Launch Services Program provides oversight of launch operations and countdown management for its uncrewed launches.
```"""

api_key = "61bc1aab37364618ae0df70bf5f340dd"
api_version = "2024-02-15-preview"
endpoint = "https://anankeus.openai.azure.com/"
api_chat_model = "Ananke3-1106-US-WEST"
api_embed_model = "AnankeEmbedding-US-WEST"
os.environ['AZURE_OPENAI_API_KEY'] = api_key
system_prompt = "You are an AI assistant that helps people find information."
message_text = [{"role": "system", "content": system_prompt}, {"role":"user","content": entity_prompt +content}]

# message_text = [{"role":"system","content":entity_prompt}]
# print(message_text)
client = Azure(
    api_key= api_key,  #密钥1或者密钥2选一个就行
    api_version= api_version,
    azure_endpoint= endpoint, #设定画面上的，格式如 https://xxxxx.openai.azure.com/
    chat_model_name = api_chat_model, embedding_model_name = api_embed_model
)

# result = client.chat(entity_prompt + content)
# print(result)
# print(json.loads(result))

graph_dic = {'Nodes': [['nasa', 'Organization', {'type': 'government agency'}], ['naca', 'Organization', {'type': 'government agency'}], 
            ['project_mercury', 'Project', {'type': 'space exploration'}], ['project_gemini', 'Project', {'type': 'space exploration'}], ['skylab', 'Space Station', {'type': 'space station'}], ['space_shuttle', 'Spacecraft', {'type': 'spacecraft'}], ['international_space_station', 'Space Station', {'type': 'space station'}], ['orion_spacecraft', 'Spacecraft', {'type': 'spacecraft'}], ['space_launch_system', 'Spacecraft', {'type': 'spacecraft'}], ['crewed_lunar_artemis_program', 'Program', {'type': 'space exploration'}], ['commercial_crew_spacecraft', 'Spacecraft', {'type': 'spacecraft'}], ['lunar_gateway_space_station', 'Space Station', {'type': 'space station'}], ['earth_observing_system', 'Science Mission', {'type': 'earth observation'}], ['heliophysics_research_program', 'Science Mission', {'type': 'heliophysics research'}], ['new_horizons', 'Spacecraft', {'type': 'space exploration'}], ['perseverance', 'Rover', {'type': 'planetary rover'}], ['james_webb_space_telescope', 'Space Telescope', {'type': 'space telescope'}], ['nasa_launch_services_program', 'Program', {'type': 'launch operations'}]], 
            'Relationships': [['nasa', 'succeeded_by', 'naca', {'start': 1958}], ['nasa', 'led', 'project_mercury', {'start': 1961, 'end': 1963}], ['nasa', 'led', 'project_gemini', {'start': 1965, 'end': 1966}], ['nasa', 'led', 'apollo_moon_landing_missions', {'start': 1968, 'end': 1972}], ['nasa', 'led', 'skylab', {'start': 1973, 'end': 1979}], ['nasa', 'led', 'space_shuttle', {'start': 1981, 'end': 2011}], ['nasa', 'supports', 'international_space_station', {'start': 2000}], ['nasa', 'oversees_development_of', 'orion_spacecraft', {}], ['nasa', 'oversees_development_of', 'space_launch_system', {}], ['nasa', 'oversees_development_of', 'commercial_crew_spacecraft', {}], ['nasa', 'oversees_development_of', 'lunar_gateway_space_station', {}], ['nasa', 'science_focused_on', 'earth_observing_system', {}], ['nasa', 'science_focused_on', 'heliophysics_research_program', {}], ['nasa', 'science_focused_on', 'new_horizons', {}], ['nasa', 'science_focused_on', 'perseverance', {}], ['nasa', 'science_focused_on', 'james_webb_space_telescope', {}], ['nasa', 'launch_services_provided_by', 'nasa_launch_services_program', {}]]}


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
        # print(self.names2id.get(key).get("id"))
        item.get("lock").release()

        return start_id



auto_ids = AutoIds()

doc_id = auto_ids.get_doc_ids(10)

print(doc_id)



from ananke.utils.arxiv_dump import process_pdf

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

class DocFlow(BaseObject):
    def __init__(self, size = 8000, overlap = 256, seps = ["\n\n", "\n", " ", ""], **kwargs):
        super().__init__()
        self.kwargs  = kwargs 
        self.graph = Neo4jGraph(**kwargs)
        self.vector = ChromaStorage(**kwargs)
        self.id_generator = AutoIds(**kwargs)
        self.splitter = RecursiveCharacterTextSplitter(chunk_size = size, chunk_overlap = overlap, separators = seps)
        self.entity_prompt = entity_prompt
        self.vector.create_collection("all-chunk")
        self.vector.create_collection("all-sent")

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
            print("props: {}-{}".format(propertys, type(propertys)))
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
        time.sleep(3)
        open_ai = Azure(self.kwargs.get("api_key"), self.kwargs.get("api_version"), azure_endpoint = self.kwargs.get("endpoint"))
        chat_response = open_ai.chat(self.entity_prompt + text)
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

    def get_chunks_triples(self, chunks: List[Chunk]):
        chunk_triples = []
        for chunk in chunks:
            summary = self.get_chunk_summary(chunk.chunk_text)
            summary = json.loads(summary)

            if summary is None or len(summary.keys()) == 0:
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
            sent.triples = triples
            sent_trples.extend(triples)

        self.graph.insert(sent_trples)

        return sent_trples


    def search(self, user_text: str, mode = "and"):
        ret = None
        user_emb = self.get_embedding(user_text)
        search_chunks = self.vector.query("all-chunk", user_emb, top_n = 50)
        search_sents = self.vector.query("all-sent", user_emb, top_n = 50)

        # print(search_chunks.keys())
        # print(search_sents.keys())
        # for item in search_chunks:

        sent_metas = search_sents.get("metadatas")
        best_meta = sent_metas[0][0]
        best_sent_id, best_chunk_id, best_doc_id = best_meta.get("sent_id"), best_meta.get("chunk_id"), best_meta.get("doc_id")

        chunk_metas = search_chunks.get("metadatas")[0]
        chunk_docs  = search_chunks.get("documents")
        for meta, doc in zip(chunk_metas, chunk_docs):
            if best_chunk_id == meta.get("chunk_id"):
                ret = doc
                break

        print("type:{}".format(type(ret)))
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



doc_flow = DocFlow(size = 1024, **dic)
path = "example/data/gpt3.pdf"
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
doc_flow.get_sents_triples(sents)