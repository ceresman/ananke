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
    uuid: str
    relation_emb_id: int

@dataclass
class Triple:
    triple_id: int
    triple_uuid: str
    sub: Entity
    pred: Relation
    obj: Entity

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
        entity.propertys["entity_uuid"] = entity.entity_uuid
        entity.propertys["entity_id"] = entity.entity_id
        entity.propertys["entity_emb_id"] = entity.entity_emb_id
        if entity.descriptions is not None:
            entity.propertys["desc"] = "".join(entity.descriptions)

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

from openai import AzureOpenAI

class AzureOpenAILLM(object):
    def __init__(
        self,
        api_key=None,
        api_version=None,
        azure_endpoint=None,
        tokenizer=None,
        max_token=8192,
        chat_model_name="Ananke",
        embedding_model_name="AnankeEmbedding",
        system_prompt="You are a helpful assistant.",
    ):
        self.api_key = api_key
        self.api_version = api_version
        self.azure_endpoint = azure_endpoint
        print(self.api_key, self.api_version, self.azure_endpoint)
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.azure_endpoint,
        )
        self.conversation = [{"role": "system", "content": system_prompt}]
        self.max_token = max_token
        self.chat_model = chat_model_name
        self.embedding_model = embedding_model_name

    def chat(self, user_input):
        self.conversation.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model=self.chat_model, messages=self.conversation
        )

        self.conversation.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )

        return response.choices[0].message.content

    def normalize_text(self, s, sep_token="\n "):
        s = re.sub(r"\s+", " ", s).strip()
        s = re.sub(r". ,", "", s)
        s = s.replace("..", ".")
        s = s.replace(". .", ".")
        s = s.replace("\n", "")
        s = s.strip()
        return s

    def embedding(self, text: str):
        text = self.normalize_text(text)
        embedding = (
            self.client.embeddings.create(input=[text], model=self.embedding_model)
            .data[0]
            .embedding
        )
        print(len(embedding))
        return embedding



# Ananke4-1106-US-WEST:
# - ENDPOINT : "https://anankeus.openai.azure.com/"
# - KEY : "45d24fc4b19047eaa81632eb76dc0fa9"
# - API_VERSION : "2024-02-15-preview"
# - API_TYPE : "azure"
# - MODEL : "gpt4-turbo"
# - ENGINE : "Ananke4-1106-US-WEST"
# Ananke3-1106-US-WEST:
# - ENDPOINT : "https://anankeus.openai.azure.com/"
# - KEY : "45d24fc4b19047eaa81632eb76dc0fa9"
# - API_VERSION : "2024-02-15-preview"
# - API_TYPE : "azure"
# - MODEL : "gpt-35-turbo"
# - ENGINE : "Ananke3-1106-US-WEST"


api_chat_model = "gpt-35-turbo"
api_embed_model = "text-embedding-ada-002"

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

Nodes: 
```json
["alice", "Person", {"age": 25, "occupation": "lawyer", "name":"Alice"}], ["bob", "Person", {"occupation": "journalist", "name": "Bob"}], ["alice.com", "Webpage", {"url": "www.alice.com"}], ["bob.com", "Webpage", {"url": "www.bob.com"}]
```
Relationships: 
```json
["alice", "roommate", "bob", {"start": 2021}], ["alice", "owns", "alice.com", {}], ["bob", "owns", "bob.com", {}] 
```
OK, here is the end of the task example.
please output with the given example format. If you understand your mission rules , tell me you are ready.
"""

content = """
The below text is you need to process
```markdown
The National Aeronautics and Space Administration (NASA /ˈnæsə/) is an independent agency of the U.S. federal government responsible for the civil space program, aeronautics research, and space research. Established in 1958, NASA succeeded the National Advisory Committee for Aeronautics (NACA) to give the U.S. space development effort a distinctly civilian orientation, emphasizing peaceful applications in space science.([4])([5])([6]) NASA has since led most American space exploration, including Project Mercury, Project Gemini, the 1968–1972 Apollo Moon landing missions, the Skylab space station, and the Space Shuttle. NASA currently supports the International Space Station and oversees the development of the Orion spacecraft and the Space Launch System for the crewed lunar Artemis program, the Commercial Crew spacecraft, and the planned Lunar Gateway space station.
NASA's science is focused on: better understanding Earth through the Earth Observing System;([7]) advancing heliophysics through the efforts of the Science Mission Directorate's Heliophysics Research Program;([8]) exploring bodies throughout the Solar System with advanced robotic spacecraft such as New Horizons and planetary rovers such as Perseverance;([9]) and researching astrophysics topics, such as the Big Bang, through the James Webb Space Telescope, and the Great Observatories and associated programs.([10]) NASA's Launch Services Program provides oversight of launch operations and countdown management for its uncrewed launches.
```"""

api_key = "45d24fc4b19047eaa81632eb76dc0fa9"
api_version = "2024-02-15-preview"
endpoint = "https://anankeus.openai.azure.com/"
api_chat_model = "gpt-35-turbo"
api_embed_model = "text-embedding-ada-002"
openai = AzureOpenAILLM(api_key = api_key, api_version = api_version, azure_endpoint = endpoint, 
        chat_model_name = api_chat_model, embedding_model_name = api_embed_model, system_prompt = entity_prompt)


entity_str = openai.chat(content)
print(entity_str)

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

api_key = "45d24fc4b19047eaa81632eb76dc0fa9"
api_version = "2024-02-15-preview"
endpoint = "https://anankeus.openai.azure.com/"
client = AzureOpenAI(
    api_key= api_key,  #密钥1或者密钥2选一个就行
    api_version= api_version,
    azure_endpoint= endpoint, #设定画面上的，格式如 https://xxxxx.openai.azure.com/
    # azure_ad_token_provider=token_provider,
)


message_text = [{"role":"system","content":"You are an AI assistant that helps people find information."},
    {"role":"user","content":"长城有多长？"}]

chat_completion = client.chat.completions.create(
    model = "gpt4-turbo",      #这个地方是要你设定的deployment_name，不是具体的模型名称，也可以是基于gpt4创建的部署名
    messages = message_text
)

print(chat_completion.choices[0].message.content)


api_version = "2023-07-01-preview"

# gets the API Key from environment variable AZURE_OPENAI_API_KEY
client = AzureOpenAI(
    api_version=api_version,
    # https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource
    azure_endpoint="https://example-endpoint.openai.azure.com",
)

completion = client.chat.completions.create(
    model="deployment-name",  # e.g. gpt-35-instant
    messages=[
        {
            "role": "user",
            "content": "How do I output all files in a directory using Python?",
        },
    ],
)
print(completion.model_dump_json(indent=2))
