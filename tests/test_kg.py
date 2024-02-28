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

sub = Entity("英雄", "张无忌", {"hy": [1111111,  2222222]}, "1024", 1, 1)
obj = Entity('派别', "明教", {}, "1025", 2, 2)
pred = Relation("属于", "一种归属描述", 3, "1025", 3)
triple = Triple(11, "11", sub, pred, obj)

sub2 = Entity("英雄", "张翠山", {}, "1024", 12, 12)
obj2 = Entity('派别', "武当山", {}, "1025", 22, 22)
pred2 = Relation("属于", "一种归属描述", 32, "10252", 32)
triple2 = Triple(22, "22", sub2, pred2, obj2)

kg.insert([triple, triple2])