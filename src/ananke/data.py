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

from ananke.base.base_object import BaseChunk,BaseDocument,BaseFile,BaseMedia,BaseMeta,BaseRelation,BaseNode


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
        
        
        self.metadata = None
        self.graph = None
        self.vector = None
        self.relation_db_index = None
        self.chunk_id = None
        self.chunk_type = None
        self.chunk_content = None
        self.chunk_content_type = None
        self.chunk_content_encoding = None
        self.chunk_content_language = None
        self.chunk_content_length = None
        self.chunk_content_encoding = None
        
        