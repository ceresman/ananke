# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __init__.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Winshare Tom <tanwenxuan@live.com>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/09/29 22:42:10 by Winshare To       #+#    #+#              #
#    Updated: 2023/12/02 19:36:01 by Winshare To      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ananke.data.utils import get_loader
from ananke.base import BaseContext,BaseObject,BaseDocument
# ---------------------------------------------------------------------------- #
#                               ananke data unit                               #
# ---------------------------------------------------------------------------- #

import json
import uuid
from uuid import UUID

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

# ----------------------------------- type ----------------------------------- #

import z3
import sympy as sp
import numpy as np
import scipy as sc

# --------------------------- logic & math library --------------------------- #


@dataclass
class LogicExpression(BaseObject):
    """
    Represents a logical expression.

    Attributes:
        expression_id (UUID): Unique identifier for the logic expression.
        expression_z3 (z3.ExprRef): The logic expression as a z3 expression.
        expression_sympy (sp.Expr): The logic expression as a SymPy expression.
    """

    expression_id: int
    expression_uuid: str
    expression_z3: z3.ExprRef
    expression_sympy: sp.Expr


@dataclass
class StructuredData(BaseObject):
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


@dataclass
class MathExpression(BaseObject):
    """
    Represents a mathematical expression.

    Attributes:
        expression_id (UUID): Unique identifier for the math expression.
        expression_latex (str): The math expression as a LaTeX string.
        expression_sympy (sp.Expr): The math expression as a SymPy expression.
        expression_wolfram (str): The math expression as a Wolfram language string.
    """

    expression_uuid: str
    expression_id: int
    expression_latex: str
    expression_sympy: sp.Expr
    expression_wolfram: str

@dataclass
class Props:
    id: int
    uid: int
    uuid: str
    genre: int # 0 - triple 1 - sub  2 - obj  3 - pred
    doc_id: int
    chunk_id: int
    sent_id: int
    emb_id: int    
    descs: List[str] = None

@dataclass
class Entity:
    label: str
    name:  str
    propertys: dict

@dataclass
class Relation:
    label: str
    name:  str
    propertys: dict

@dataclass
class Triple:
    triple_id: int
    triple_uuid: str
    sub: Entity
    pred: Relation
    obj: Entity

@dataclass
class Sentence:
    sent_uuid: str
    sent_id: int
    sent_text: str
    sent_emb_id: int
    parent_chunk_id: int
    parent_doc_id: int
    triples: List[Triple] = None

@dataclass
class Chunk:
    chunk_uuid: str
    chunk_id : int
    chunk_text: str
    chunk_summary: str
    chunk_emb_id: int
    parent_doc_id: int
    sents: List[Sentence] = None
    triples: List[Triple] = None

@dataclass
class Meta:
    meta_id: int
    meta_uuid: str
    meta_type: str
    meta_json: str
    meta_value: dict

@dataclass
class Document:
    doc_uuid: str
    doc_id : int
    doc_text: str
    doc_meta: Meta
    doc_emb_id: int
    chunks: List[Chunk] = None

@dataclass
class EntitySemantic(BaseObject):
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
class EntitySymbol(BaseObject):
    """
    Represents a symbolic entity in the knowledge graph.

    Attributes:
        symbol_id (UUID): Unique identifier for the symbol entity.
        name (str): The name of the symbol.
        descriptions (List[str]): List of descriptions for the symbol.
        semantics (List[EntitySemantic]): List of associated semantic entities.
        property (StructuredData): Structured data representing properties.
        label (StructuredData): Structured data representing labels.
    """

    symbol_id: UUID
    name: str
    descriptions: List[str]
    semantics: List[EntitySemantic]
    propertys: List[StructuredData]
    label: List[StructuredData]


@dataclass
class RelationSemantic(BaseObject):
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
class RelationSymbol(BaseObject):
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


# @dataclass
# class Triple(BaseObject):
#     """
#     Represents a triple in the knowledge graph.

#     Attributes:
#         triple_id (UUID): Unique identifier for the triple.
#         subject (EntitySymbol): The subject entity in the triple.
#         predicate (RelationSymbol): The predicate or relationship between subject and object.
#         obj (EntitySymbol): The object entity in the triple.
#     """

#     triple_id: UUID
#     subject: EntitySymbol
#     predicate: RelationSymbol
#     obj: EntitySymbol


# ---------------------------------------------------------------------------- #
#                               File Entity Level                              #
# ---------------------------------------------------------------------------- #


@dataclass
class StructuredSentence(BaseObject):
    """
    Represents a structured sentence within a chunk.

    Attributes:
        entity_relations (List[Triple]): List of entity relations.
        logic_expressions (List[LogicExpression]): List of logic expressions.
        math_expressions (List[MathExpression]): List of math expressions.
        sentence_vectorization (np.ndarray): Vector representation of the sentence.
        parent_chunk_id (UUID): Unique identifier of the parent chunk.
        parent_doc_id (UUID): Unique identifier of the parent document.
    """

    entity_relations: List[Triple]
    logic_expressions: List[LogicExpression]
    math_expressions: List[MathExpression]
    sentence_vectorization: np.ndarray
    parent_chunk_id: UUID
    document_id: UUID


@dataclass
class StructuredChunk(BaseObject):
    """
    Represents a structured chunk within a document.

    Attributes:
        chunk_id (UUID): Unique identifier for the chunk.
        chunk_raw_content (str): Raw content of the chunk.
        chunk_summary_content (str): Automatically generated summary content.
        modality_identifier (str): Identifier for the modality.
        parent_doc_id (UUID): Unique identifier of the parent document.
        extraction_entity_results (List[EntitySymbol]): List of customized entity extraction results for the chunk.
        extraction_relation_results (List[RelationSymbol]): List of customized relation extraction results for the chunk.
        extraction_triple_results (List[Triple]): List of customized triple extraction results for the chunk.
        logic_expression_extraction_results (List[LogicExpression]): List of customized logic expression extraction results for the chunk.
        math_expression_extraction_results (List[MathExpression]): List of math expression extraction results for the chunk.
        # Add more attributes as needed.
    """

    chunk_id: UUID
    chunk_raw_content: str
    chunk_summary_content: str
    modality_identifier: str
    document_id: UUID

    extraction_entity_results: List[EntitySymbol]
    extraction_relation_results: List[RelationSymbol]
    extraction_triple_results: List[Triple]
    logic_expression_extraction_results: List[LogicExpression]
    math_expression_extraction_results: List[MathExpression]
    # Add more attributes as needed.


# @dataclass
# class Document(BaseDocument):
#     """
#     Represents a document or a file.

#     Attributes:
#         doc_id (UUID): Unique identifier for the document.
#         meta (StructuredData): Meta information about the document.
#         meta_embedding (np.ndarray): Embedding representation of the meta information.
#         raw_content (str): Raw content of the document.
#     """

#     id: UUID
#     meta: StructuredData
#     meta_embedding: np.ndarray
#     raw_content: str
#     StructuredChunks: List[StructuredChunk]


# ---------------------------------------------------------------------------- #
#                                   DATA UNIT                                  #
# ---------------------------------------------------------------------------- #


def read(filename):
    loader = get_loader(filename)
    return loader.read(filename)

@dataclass
class Context(BaseContext):
    id:UUID
    role:str
    content:str
    timestemp:str
    context_embedding:np.ndarray
    context_type:str


