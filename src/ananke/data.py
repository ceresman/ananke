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

from typing import Any
from ananke.base import BaseChunk,BaseDocument,BaseFile,BaseMedia,BaseMeta,BaseRelation,BaseNode
from dataclasses import dataclass

# ---------------------------------------------------------------------------- #
#                           Current DataType Support                           #
# ---------------------------------------------------------------------------- #


class Paper(BaseDocument):
    def __init__(self):
        super().__init__()
        self.name = "Paper"
        self.logger.info(f"Initialized {self.name}.")
        
class WordDocument(BaseDocument):
    def __init__(self):
        super().__init__()
        self.name = "WordDocument"
        self.logger.info(f"Initialized {self.name}.")
        
class ExcelDocument(BaseDocument):
    def __init__(self):
        super().__init__()
        self.name = "ExcelDocument"
        self.logger.info(f"Initialized {self.name}.")
        
class PowerPointDocument(BaseDocument):
    def __init__(self):
        super().__init__()
        self.name = "PowerPointDocument"
        self.logger.info(f"Initialized {self.name}.")
class PDFDocument(BaseDocument):
    def __init__(self):
        super().__init__()
        self.name = "PDFDocument"
        self.logger.info(f"Initialized {self.name}.")
        
class TextDocument(BaseDocument):
    def __init__(self):
        super().__init__()
        self.name = "TextDocument"
        self.logger.info(f"Initialized {self.name}.")


class MarkdownDocument(BaseDocument):
    def __init__(self):
        super().__init__()
        self.name = "MarkdownDocument"
        self.logger.info(f"Initialized {self.name}.")
        
class CSVDocument(BaseDocument):
    def __init__(self):
        super().__init__()
        self.name = "CSVDocument"
        self.logger.info(f"Initialized {self.name}.")
        
        
class WebPageDocument(BaseDocument):
    def __init__(self):
        super().__init__()
        self.name = "WebPageDocument"
        self.logger.info(f"Initialized {self.name}.")
        
class ImageDocument(BaseMedia):
    def __init__(self):
        super().__init__()
        self.name = "ImageDocument"
        self.logger.info(f"Initialized {self.name}.")
                
class VideoDocument(BaseMedia):
    def __init__(self):
        super().__init__()
        self.name = "VideoDocument"
        self.logger.info(f"Initialized {self.name}.")
                
class AudioDocument(BaseMedia):
    def __init__(self):
        super().__init__()
        self.name = "AudioDocument"
        self.logger.info(f"Initialized {self.name}.")
        
class CodeDocument(BaseDocument):
    def __init__(self):
        super().__init__()
        self.name = "CodeDocument"
        self.logger.info(f"Initialized {self.name}.")
        
class LaTeXDocument(BaseDocument):
    def __init__(self):
        super().__init__()
        self.name = "LaTeXDocument"
        self.logger.info(f"Initialized {self.name}.")
        
        

# TODO: Add more file types        
        
# class BinaryDocument(BaseDocument):
#     def __init__(self):
#         super().__init__()
#         self.name = "BinaryDocument"
#         self.logger.info(f"Initialized {self.name}.")
        
# class ExecutableDocument(BaseDocument):
#     def __init__(self):
#         super().__init__()
#         self.name = "ExecutableDocument"
#         self.logger.info(f"Initialized {self.name}.")
   
# class CompressedDocument(BaseDocument):
#     def __init__(self):
#         super().__init__()
#         self.name = "CompressedDocument"
#         self.logger.info(f"Initialized {self.name}.")
        
# class EncryptedDocument(BaseDocument):
#     def __init__(self):
#         super().__init__()
#         self.name = "EncryptedDocument"
#         self.logger.info(f"Initialized {self.name}.")


# ---------------------------------------------------------------------------- #
#                                 Core DataType                                #
# ---------------------------------------------------------------------------- #



@dataclass
class structed_chunk:
    metadata: dict = None
    graph: Any = None
    vector: Any = None
    relation_db_index: Any = None
    chunk_id: Any = None
    chunk_type: Any = None
    chunk_content: Any = None
    chunk_content_type: Any = None
    chunk_content_encoding: Any = None
    chunk_content_language: Any = None
    chunk_content_length: Any = None
    chunk_content_encoding: Any = None




        
class StructuredChunks(BaseChunk):
    def __init__(self):
        """
        > chunks are the basic unit of data storage in Ananke.
        Include all kinds of data, such as text, image, video, audio, etc.
        In normal cases, chunks are stored in a structured way.
        The core goal is use chunk group graph/vector/relational database can be indexed and searched.
        ****
        * metadata: structured data that describes the chunk, such as title, author, etc. 
        normally parse from document and media subject.
        * graph: structured data that describes the relationship & nodes this chunk. 
        need to be formatted by neo4j ot nebula style.
        * vector: embedding of the chunk, normally generated by deep learning model.
        * relation_db_index: index of the chunk in relation database, normally generated by uuid.
        * chunk_id: unique id of the chunk, normally generated by uuid.
        * chunk_type: type of the chunk, normally define by loader.
        * chunk_content: content of the chunk.
        """
        super().__init__()
        self.name = "StructuredChunks"
        self.logger.info(f"Initialized {self.name}.")
        self.batch = []
    
    
    
    
    # ---------------------------------------------------------------------------- #
    #                                   Operation                                  #
    # ---------------------------------------------------------------------------- #
    
    
        
    def __str__(self):
        return f"StructuredChunks({self.chunk_id})"
    
    def __repr__(self):
        return f"StructuredChunks({self.chunk_id})"
    
    def __eq__(self, other):
        return self.chunk_id == other.chunk_id
    
    def __hash__(self):
        return hash(self.chunk_id)
    
    def __lt__(self, other):
        return self.chunk_id < other.chunk_id
    
    def __gt__(self, other):
        return self.chunk_id > other.chunk_id
    
    def __le__(self, other):
        return self.chunk_id <= other.chunk_id
    def __ge__(self, other):
        return self.chunk_id >= other.chunk_id
    def __ne__(self, other):
        return self.chunk_id != other.chunk_id
    def __contains__(self, item):
        return item in self.chunk_content
    def __len__(self):
        return len(self.chunk_content)
    
    def __getitem__(self, item):
        return self.chunk_content[item]
    def __setitem__(self, key, value):
        self.chunk_content[key] = value
        
    def __delitem__(self, key):
        del self.chunk_content[key]
    def __iter__(self):
        return iter(self.chunk_content)    
    
    def __name__(self):
        return self.name