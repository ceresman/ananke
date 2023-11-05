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
from ananke.base import BaseChunk
from dataclasses import dataclass
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

from uuid import UUID
# ---------------------------------------------------------------------------- #
#                   Logic / Math Symbol & Reasoning Computing                  #
# ---------------------------------------------------------------------------- #
import z3
import sympy as sp
import numpy as np
import scipy as sc




# ---------------------------------------------------------------------------- #
#                        Semantic & Symbol System Define                       #
# ---------------------------------------------------------------------------- #

# TODO : 


@dataclass
class EntitySemantic:
    """
    Represents a semantic entity in the knowledge graph.

    Attributes:
        semantic_id (UUID): Unique identifier for the semantic entity.
        name (str): A description of the semantic entity.
        vector_representation (np.ndarray): Numerical representation of the entity.
    """
    semantic_id: UUID
    name: str
    vector_representation: np.ndarray
@dataclass
class EntitySymbol:
    """
    Represents a symbolic entity in the knowledge graph.

    Attributes:
        symbol_id (UUID): Unique identifier for the symbol entity.
        name (str): The name of the symbol.
        descriptions (List[str]): List of descriptions for the symbol.
        semantics (List[EntitySemantic]): List of associated semantic entities.
    """
    symbol_id: UUID
    name: str
    descriptions: List[str]
    semantics: List[EntitySemantic]

@dataclass
class RelationSemantic:
    """
    Represents a semantic relation in the knowledge graph.

    Attributes:
        relation_id (UUID): Unique identifier for the semantic relation.
        name (str): The name of the semantic relation.
        semantic (np.ndarray): Numerical representation of the relation.
    """
    relation_id: UUID
    name: str
    semantic: np.ndarray

@dataclass
class RelationSymbol:
    """
    Represents a symbol representing a relation in the knowledge graph.

    Attributes:
        relation_id (UUID): Unique identifier for the relation symbol.
        name (str): The name of the relation symbol.
        description (str): Description of the relation symbol.
        semantics (RelationSemantic): Associated semantic representations for the relation.
    """
    relation_id: UUID
    name: str
    description: str
    semantics: RelationSemantic

@dataclass
class LogicExpression:
    """
    Represents a logical expression.

    Attributes:
        expression_id (UUID): Unique identifier for the logic expression.
        expression_z3 (z3.ExprRef): The logic expression as a z3 expression.
        expression_sympy (sympy.Expr): The logic expression as a SymPy expression.
    """
    expression_id: UUID
    expression_z3: z3.ExprRef
    expression_sympy: sp.Expr

@dataclass
class MathExpression:
    """
    Represents a mathematical expression.

    Attributes:
        expression_id (UUID): Unique identifier for the math expression.
        expression_latex (str): The math expression as a LaTeX string.
        expression_sympy (sympy.Expr): The math expression as a SymPy expression.
    """
    expression_id: UUID
    expression_latex: str
    expression_sympy: sp.Expr

@dataclass
class Triple:
    """
    Represents a triple in the knowledge graph.

    Attributes:
        triple_id (UUID): Unique identifier for the triple.
        subject (EntitySymbol): The subject entity in the triple.
        predicate (RelationSymbol): The predicate or relationship between subject and object.
        obj (EntitySymbol): The object entity in the triple.
    """
    triple_id: UUID
    subject: EntitySymbol
    predicate: RelationSymbol
    obj: EntitySymbol

@dataclass
class StructuredData:
    """
    Represents structured data.

    Attributes:
        data_id (UUID): Unique identifier for the structured data.
        data_type (str): Type of structured data (e.g., "text," "image," etc.).
        data_value (dict): The actual data value (e.g., the text content or image data).
    """
    data_id: UUID
    data_type: str
    data_value: dict
    
    
    
    

# ---------------------------------------------------------------------------- #
#                                 Core DataType                                #
# ---------------------------------------------------------------------------- #



# 原文语义分割级别的chunk，作为在向量体系中被一级索引的最基本单元。
# 设计至关重要，在整体的索引关系上大致为(暂时性定义)

# 1.（Class Document）文档/文件级别：
# - 关系性索引唯一标识符-（UUID）
# - meta
# - meta embedding
# - raw content

# 2.(Class StructuredChunk)针真对raw content得splited chunks级别

# - chunk唯一标识索引（UUID）
# - chunk raw content
# - chunk summary content（auto meta）
# - 模态标识符
# - 父文档唯一标识符（UUID）
# - chunk level 定制化的实体抽取结果列表
# - chunk level 定制化的关系抽取结果列表
# - chunk level 定制化的三元组抽取结果列表

# - chunk level 定制化的逻辑表达式抽取结果列表
# - chunk level 数学表达式抽取结果列表
# - ...

# 3.(Class StructuredSentence)真对单个chunk语义分句级别

# - 实体关系，如果在chunk级别的实体关系中已经出现则不添加
# - 逻辑表达式，同理，需要和chunk级别做重复性和逻辑冲突性校验
# - 数学表达式
# - 语句向量化
# - 父chunk唯一标识符（UUID）
# - 父文档唯一标识符（UUID）

# TODO ： 

# ---------------------------------------------------------------------------- #
#                                  TEMPDEFINE                                  #
# ---------------------------------------------------------------------------- #
@dataclass
class Document:
    """
    Represents a document or file.


    Attributes:
        doc_id (UUID): Unique identifier for the document.
        meta: Meta information about the document.
        meta_embedding: Embedding representation of the meta information.
        raw_content: Raw content of the document.
    """
    doc_id: UUID
    meta: StructuredData  # Replaced 'str' with 'EntitySemantic'
    meta_embedding: np.ndarray
    raw_content: str

@dataclass
class StructuredChunk:
    """
    Represents a structured chunk within a document.


    Attributes:
        chunk_id (UUID): Unique identifier for the chunk.
        chunk_raw_content: Raw content of the chunk.
        chunk_summary_content: Automatically generated summary content.
        modality_identifier: Identifier for the modality.
        parent_doc_id (UUID): Unique identifier of the parent document.
        entity_extraction_results: List of customized entity extraction results for the chunk.
        logic_expression_extraction_results: List of customized logic expression extraction results for the chunk.
        math_expression_extraction_results: List of math expression extraction results for the chunk.
        # Add more attributes as needed.
    """
    chunk_id: UUID
    chunk_raw_content: str
    chunk_summary_content: str
    modality_identifier: str
    parent_doc_id: UUID
    
    extraction_entity_results: List[EntitySymbol]  # Replaced 'str' with 'EntitySymbol'
    extraction_relation_results: List[RelationSymbol]  # Replaced 'str' with 'EntitySymbol'
    extraction_triple_results: List[EntitySymbol]  # Replaced 'str' with 'EntitySymbol'
    
    # ------------------------------------- — ------------------------------------ #
    logic_expression_extraction_results: List[LogicExpression]  # Replaced 'str' with 'LogicExpression'
    math_expression_extraction_results: List[MathExpression]  # Replaced 'str' with 'MathExpression'
    
    # Add more attributes as needed.

@dataclass
class StructuredSentence:
    """
    Represents a structured sentence within a chunk.


    Attributes:
        entity_relations: List of entity relations.
        logic_expressions: List of logic expressions.
        math_expressions: List of math expressions.
        sentence_vectorization: Vector representation of the sentence.
        parent_chunk_id (UUID): Unique identifier of the parent chunk.
        parent_doc_id (UUID): Unique identifier of the parent document.
    """
    entity_relations: List[Triple]  # Replaced 'str' with 'Triple'
    logic_expressions: List[LogicExpression]  # Replaced 'str' with 'LogicExpression'
    math_expressions: List[MathExpression]  # Replaced 'str' with 'MathExpression'
    sentence_vectorization: np.ndarray
    parent_chunk_id: UUID
    parent_doc_id: UUID