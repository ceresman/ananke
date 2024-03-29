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

from ananke.db import vector_storage
import chromadb

class ChromaStorage(vector_storage):
    def __init__(self,**kwargs):
        super().__init__()
        self.name = "ChromaStorage"
        self.collection_cache = {}
        self.path = kwargs.get("vector_db_path", "./chromadb")
        self.vector_db = chromadb.PersistentClient(self.path)
        self.logger.info(f"Initialized {self.name}.")


    def delete_collection(self, name):
        self.collection_cache[name].delete_collection()
        self.collection_cache[name] = None

    def create_collection(self, name):
        if self.collection_cache.get(name, None) is None:
            collection = self.vector_db.get_or_create_collection(name, metadata = {"hnsw:space": "cosine"})
            self.collection_cache[name] = collection
            return

        logger.error("duplicate collection name {}".format(name))

    def add(self, name, embs, metadatas, ids, docs):
        collection = self.collection_cache.get(name, None)
        if collection is None:
            try:
                collection = self.db.get_collection(name = name)
                self.collection_cache[name] = collection
            except Exception as e:
                self.logger.error("collection name {} not exist".format(name))
                return

        if len(metadatas) == 0:
            metadatas = [{"id": item} for item in ids]

        ids = [str(item) for item in ids]
        collection.add(embeddings = embs, documents = docs, metadatas = metadatas, ids = ids)
        

    def query(self, name, embs, top_n = 100, filters = {}):
        collection = self.collection_cache.get(name)
        if collection is None:
            self.logger.error("collection name {} not exist".format(name))
            return None

        return collection.query(query_embeddings = [embs], n_results = top_n, where = filters)


class MilvusStorage(vector_storage):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = "MilvusStorage"
        self.logger.info(f"Initialized {self.name}.")
        self.collection_cache = {}

    def create_collection(self, name):
        pass

    def add(self, name, embs, metadatas):
        pass

    def search(self, name, embs, metadatas, filters):
        pass

