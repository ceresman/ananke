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

from ananke.db import kg_storage
from ananke.data import Triple, Entity

class Neo4jStorage(kg_storage):
    def __init__(self,**kwargs):
        import py2neo
        from py2neo import Graph, Node, Relationship, NodeMatch
        super().__init__()
        self.type = "Neo4jStorage"
        self.logger.info(f"Initialized {self.type}.")
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

    def search(self):
        pass

class NebulaStorage(kg_storage):
    def __init__(self,**kwargs):
        from nebula3.Config import SessionPoolConfig
        from nebula3.gclient.net.SessionPool import SessionPool
        super().__init__()
        self.type = "NebulaStorage"
        self.logger.info(f"Initialized {self.type}.")
        self.host = kwargs.get("kg_host")
        self.port = kwargs.get("kg_port")
        self.user = kwargs.get("kg_user")
        self.passwd = kwargs.get("kg_passwd")
        self.db = kwargs.get("kg_db")
        session_pool = SessionPool(self.user, self.passwd, self.db, [(self.host, int(self.port))])
        seesion_pool_config = SessionPoolConfig()
        session_pool.init(seesion_pool_config)
        self.session_pool = session_pool

    def insert(self, triples:List[Triple]):
        tags, edges = [], {}
        tag_props = {}

        for triple in triples:
            sub_label, obj_label = triple.sub.label, triple.obj.label
            edge_type = triple.pred.name
            tags.append(sub_label)
            tags.append(obj_label)
            edges.append(edge_type)

            if sub_label== obj_label:
                if sub_label not in tag_props.keys():
                    props = {**triple.sub.label.propertys, **triple.obj.label.propertys}
                    tag_props[sub_label] = props
                else:
                    props = {**triple.sub.label.propertys, **triple.obj.label.propertys}
                    tag_props[sub_label] = {**props, **tag_props[sub_label]}
            else:
                if sub_label in tag_props.keys():
                   tag_props[sub_label] = {**triple.sub.label.propertys, **tag_props[sub_label]}
                else:
                   tag_props[sub_label] = {**triple.sub.label.propertys}
                if obj_label in tag_props.keys():
                   tag_props[obj_label] = {**triple.obj.label.propertys, **tag_props[obj_label]}
                else:
                   tag_props[obj_label] = {**triple.obj.label.propertys}

        tags = list(set(tags))
        edges = list(set(edges))

        tag_str_props = {}
        for tag in tags:
            props = []
            for tag in tag_props.keys():
                props.append(tag + " " + type(tag_props[tag]))
            props = ",".join(props)
            props = "(" + props + ")"
            tag_str_props[tag] = props
            query = "'CREATE TAG IF NOT EXISTS {}{}'".format(tag, props)
            self.session_pool.excute(query)

        for edge in edges:
            props = "(description string)"
            query = "'CREATE EDGE IF NOT EXISTS {}{}'".format(edge, props)
            self.session_pool.excute(query)

        for triple in triples:
            self.add_entity(triple.sub, tag_str_props[triple.sub.label], tag_props[triple.sub.label])
            self.add_entity(triple.obj, tag_str_props[triple.obj.label], tag_props[triple.obj.label])
            self.add_edge(triple.sub.entity_id, triple.obj.entity_id, triple.pred.name, triple.pred.description)

        return

    def add_entity(self, entity: Entiy, entity_label_props, prop_names):
        entity_label = entity.label
        entity_id = entity.entity_id
        entity_props = entity.propertys
        query = self.get_entity_query(entity_label, entity_id, entity_label_props, entity_props, prop_names)
        self.session_pool.excute(query)

    def get_entity_query(self, entity_label, entity_label_id, entity_label_props, entity_props, prop_names):
        props = []
        for name in prop_names:
            value = entity_props.get(name)
            if type(value) == str:
                props.append('"{}"'.format(value))
            if type(value) == int:
                props.append('{}'.format(value))
        props_value = ",".join(props)
        props_value = "(" + props + ")"
        query = "'INSERT VERTEX IF NOT EXISTS {}{} VALUES "{}":{}'".format(entity_label, entity_label_props, entity_label_id, props_value)
        return query

    def add_edge(self, sub_id, obj_id, realtion, desc:str):
        query = "'INSERT EDGE IF NOT EXISTS {}({}) VALUES "{}"->"{}":("{}")'".format(realtion, desc, str(sub_id), str(obj_id))
        self.session_pool.excute(query)
