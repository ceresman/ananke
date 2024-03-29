from ananke.base import BaseObject
from nltk.tokenize import sent_tokenize
from ananke.data import Entity, Relation, Triple
from ananke.data import Chunk, Document,Sentence, Meta
from ananke.llm.azure import Azure
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ananke.db.vector import ChromaStorage
from utils.client_manager import client_get, client_set
from utils.nodes import is_real_nodes, update_nodes_rels
from utils.tools import init_redis_single
from utils.log import logger
import threading, json

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

class AutoIds(object):
    def __init__(self, **kwargs):
        self.doc = {"id": 1, "emb_id": 1, "lock": threading.Lock()}
        self.chunk = {"id": 1, "emb_id": 1, "lock": threading.Lock()}
        self.sent = {"id": 1, "emb_id": 1, "lock": threading.Lock()}
        self.node = {"id": 1, "emb_id": 1, "lock": threading.Lock()}
        self.rel = {"id": 1, "emb_id": 1, "lock": threading.Lock()}
        self.triple = {"id": 1, "emb_id": 1, "lock": threading.Lock()}

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
        start_id = 1
        item = self.names2id.get(key)
        key = "auto_id:" + key
        item.get("lock").acquire()
        redis = client_get("redis")
        start_id = redis.get(key)
        if start_id is None:
            start_id = 1
        redis.set(key, str(int(start_id) + length))
        item.get("lock").release()
        return int(start_id)

class DocFlow(BaseObject):
    def __init__(self, size = 8000, overlap = 256, seps = ["\n\n", "\n", " ", ""], **kwargs):
        super().__init__(**kwargs)
        self.kwargs  = kwargs 
        # self.graph = Neo4jGraph(**kwargs)
        self.vector = ChromaStorage(**kwargs)
        self.id_generator = AutoIds(**kwargs)
        self.splitter = RecursiveCharacterTextSplitter(chunk_size = 8000, chunk_overlap = 256, separators = ["\n\n", "\n", " ", ""])
        self.entity_prompt = entity_prompt
        self.vector.create_collection("all-chunk")
        self.vector.create_collection("all-sent")
        self.vector.create_collection("user-chunk")
        self.vector.create_collection("user-phase")
        self.vector.create_collection("all-phase")
        self.auto_ids = AutoIds(**kwargs)
        self.datas = {}

    def set_splitter(self, size = 8000, overlap = 256, seps = ["\n\n", "\n", " ", ""]):
        self.splitter = RecursiveCharacterTextSplitter(chunk_size = size, chunk_overlap = overlap, separators = seps)


    def get_embedding(self, text):
        open_ai = Azure(self.kwargs.get("api_key"), self.kwargs.get("api_version"), azure_endpoint = self.kwargs.get("endpoint"))
        embedding = open_ai.embedding(text)
        return embedding

    def get_entity_response(self, text):
        open_ai = Azure(self.kwargs.get("api_key"), self.kwargs.get("api_version"), azure_endpoint = self.kwargs.get("endpoint"))
        # self.logger.info("entity-input:{}".format(self.entity_prompt + text))
        chat_response = open_ai.get_entity(self.entity_prompt + text)
        return chat_response

    def get_sent_summary(self, text):
        return self.get_entity_response(text)

    def get_chunk_summary(self, text):
        return self.get_entity_response(text)

    def get_noun_words(self, doc_id, nodes_dic, rels_dic, tenant = "all"):
        noun_words = []
        for key in nodes_dic.keys():
            noun_words.append(key)
            noun_words.extend(list(nodes_dic[key].keys()))
        
        for key in rels_dic.keys():
            noun_words.append(key)
            noun_words.extend(list(rels_dic[key].keys()))

        noun_words = list(set(noun_words))

        metas, words, embeddings, emb_ids = [], [], [], []
        start_id = self.id_generator.get_sent_ids(len(noun_words))
        for ix, word in enumerate(noun_words, start = start_id):
            try:
                embedding = self.get_embedding(word)

                embeddings.append(embedding)
                emb_ids.append(ix)
                words.append(word)
                metas.append({"doc_id": doc_id, "word": word})
            except Exception as e:
                logger.error("Exception is {}, word is {}".format(e, word))

        self.vector.add(tenant + "-phase", embeddings, metas, emb_ids, words)
        return noun_words

    def get_chunks(self, pdf_id, page_data:dict, tenant = "all"):
        noun_words = []
        nodes_dic, rels_dic = {}, {}
        emb_ids, metas, embeddings, texts = [], [], [], []

        for page_id in page_data.keys():
            page_text = page_data[page_id]
            raw_texts = self.splitter.split_text(page_text)
            start_id = self.id_generator.get_chunk_ids(len(raw_texts))
            for chunk_id, raw_text in enumerate(raw_texts, start = start_id):
                emb_ids.append(chunk_id)
                metas.append({"doc_id": pdf_id, "chunk_id": chunk_id, "page_id": page_id})
                texts.append(raw_text)
                embeddings.append(self.get_embedding(raw_text))

                summary = self.get_chunk_summary(raw_text)
                if summary is None:
                    logger.info("summary is {}".format(summary))
                    continue

                try:
                    summary = json.loads(summary)
                    summary = {key.lower() : summary[key] for key in summary.keys()}
                    if not is_real_nodes(summary):
                        continue

                    update_nodes_rels(nodes_dic, rels_dic, summary)
                except Exception as e:
                    logger.info("chunk except is {}, summary is {}".format(e, summary))

        
        self.vector.add(tenant + "-chunk", embeddings, metas, emb_ids, texts)
        noun_words = self.get_noun_words(pdf_id, nodes_dic, rels_dic, tenant)
        self.datas[pdf_id] = [noun_words, nodes_dic, rels_dic]

        self.set2redis("nodes", pdf_id, json.dumps(nodes_dic))
        self.set2redis("rels", pdf_id, json.dumps(rels_dic))
        self.set2redis("words", pdf_id, json.dumps(noun_words))

    def set2redis(self, key, pdf_id, value):
        redis = client_get("redis")
        for i in range(0, 3):
            try:
                redis_key = "data:" + key + ":" + pdf_id 
                redis.set(redis_key, value)
            except Exception as e:
                logger.info("set except e:{}".format(e))
                config = client_get("config")
                redis = init_redis_single(config.get("redis-hostport"), config.get("redis-password"))
                time.sleep(3)
                client_set("redis", redis)

    def get_from_redis(self, key, pdf_id):
        redis = client_get("redis")
        for i in range(0, 3):
            try:
                redis_key = "data:" + key + ":" + pdf_id
                value = redis.get(redis_key)
                if value is not None:
                    value = json.loads(value)
                else:
                    value = {}

                return value
            except Exception as e:
                config = client_get("config")
                redis = init_redis_single(config.get("redis-hostport"), config.get("redis-password"))
                time.sleep(3)
                client_set("redis", redis)
        return {}

    def get_relevant(self, searchs, threshold):
        result = []
        ids = searchs.get("ids")[0]
        distances = searchs.get("distances")[0]
        documents = searchs.get("documents")[0]
        metas = searchs.get("metadatas")[0]
        for ix, item in enumerate(searchs.get("distances")[0], start = 0):
            if item <= threshold:
                result.append({"id": ids[ix], "metadata": metas[ix], "dis": distances[ix], "documents": documents[ix]})

        return result
        
    def search(self, pdf_id:str, text:str, threshold = 0.2):
        logger.info("pdf_id is {}, text is {}".format(pdf_id, text))        

        nodes_dic = self.get_from_redis("nodes", pdf_id)
        rels_dic = self.get_from_redis("rels", pdf_id)
        words = self.get_from_redis("words", pdf_id)

        user_emb = self.get_embedding(text)
        user_chunks = self.vector.query("user-chunk", user_emb, top_n = 50, filters = {"doc_id": pdf_id})
        user_words = self.vector.query("user-phase", user_emb, top_n = 50, filters = {"doc_id": pdf_id})
        all_chunks = self.vector.query("all-chunk", user_emb, top_n = 50)
        all_words = self.vector.query("all-phase", user_emb, top_n = 50)

        # logger.info("user-chunk: {}".format(user_chunks.get("distances")))
        # logger.info("user-words: {}".format(type(user_words)))
        # logger.info("all-chunk: {}".format(all_words.get("distances")))
        # logger.info("all-words: {}".format(all_chunks.get("distances")))

        user_chunks = self.get_relevant(user_chunks, threshold)
        user_words = self.get_relevant(user_words, threshold)
        all_chunks = self.get_relevant(all_chunks, threshold)
        all_words = self.get_relevant(all_words, threshold)

        result = {"pdf_id": pdf_id, "self": {"chunks": user_chunks, "phase": user_words}, "relevant": {"chunks": all_chunks, "words": all_words}}
        return result

    def get_docs(self, doc_paths, tenant = "all"):
        pass


# //2024_03_28_af0dc41784cf60efecabg
# 2024_03_28_d918ce007641daed7730g.html