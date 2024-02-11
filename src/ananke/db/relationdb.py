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

from ananke.db import relation_storage


class RedisStorage(relation_storage):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "RedisStorage"
        self.logger.info(f"Initialized {self.type}.")
        


class SqliteStorage(relation_storage):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "SqliteStorage"
        self.logger.info(f"Initialized {self.type}.")
        
    
        
class MariaDBStorage(relation_storage):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "MariaDBStorage"
        self.logger.info(f"Initialized {self.type}.")
        
        
class MySQL(relation_storage):
    def __init__(self, **kwargs):
        super().__init__()
        self.type = "MariaDBStorage"
        self.logger.info(f"Initialized {self.type}.")
        self.host = kwargs.get("msyql_host")
        self.user = kwargs.get("mysql_user")
        self.passwd = kwargs.get("msyql_passwd")
        self.db_name = kwargs.get("mysql_db", "ananke")
        self.port = kwargs.get("mysql_port", 3306)
        self.conn = pymysql.connect(host = self.host, user = self.user, passwd = self.passwd,
                    port = self.port, database = self.db_name, charset='utf8')
        self.batch = 128

    def insert_data(self, sql, data):
        cursor = self.conn.cursor()
        cursor.executemany(sql, data)
        self.conn.commit()
        auto_incre_id = cursor.lastrowid
        cursor.close()
        return auto_incre_id

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

        return docs

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

        return chunks


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

        return sent

    def insert_logic(self):
        pass

    def insert_math(self):
        pass

    def update_logci(self):
        pass
    def update_match(self):
        pass

    def delete_logic(self):
        pass