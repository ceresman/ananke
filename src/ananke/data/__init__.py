# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __init__.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Winshare Tom <tanwenxuan@live.com>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/09/29 22:42:10 by Winshare To       #+#    #+#              #
#    Updated: 2023/10/01 18:21:37 by Winshare To      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from typing import Any
from dataclasses import dataclass

from ananke.data.code import CodeDocument
from ananke.data.general import *
from ananke.data.media import *
from ananke.data.structure import *

import re
import json
import os

DOCUMENTS = {
    "Paper": Paper,
    "WordDocument": WordDocument,
    "ExcelDocument": ExcelDocument,
    "PowerPointDocument": PowerPointDocument,
    "PDFDocument": PDFDocument,
    "TextDocument": TextDocument,
    "MarkdownDocument": MarkdownDocument,
    "CSVDocument": CSVDocument,
    "WebPageDocument": WebPageDocument,
    "ImageDocument": ImageDocument,
    "VideoDocument": VideoDocument,
    "AudioDocument": AudioDocument,
    "CodeDocument": CodeDocument,
    "LaTeXDocument": LaTeXDocument,
}


TYPE = {
    "Paper": r"\.pdf$",
    "WordDocument": r"\.docx$",
    "ExcelDocument": r"\.xlsx$",
    "PowerPointDocument": r"\.pptx$",
    "PDFDocument": r"\.pdf$",
    "TextDocument": r"\.txt$",
    "MarkdownDocument": r"\.md$",
    "CSVDocument": r"\.csv$",
    "WebPageDocument": r"\.html$",
    "ImageDocument": r"\.(jpg|jpeg|png|gif)$",
    "VideoDocument": r"\.(mp4|avi|mkv)$",
    "AudioDocument": r"\.(mp3|wav|ogg)$",
    "CodeDocument": r"\.(py|java|cpp|html)$",
    "LaTeXDocument": r"\.tex$",
}

# 定义一个函数，根据文件名获取文件类型
def get_file_type(file_name):
    """get file type from file name

    Args:
        file_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    for doc_type, pattern in TYPE.items():
        if re.search(pattern, file_name, re.IGNORECASE):
            return doc_type
    return None

# 定义一个函数，根据文件名获取相应的类
def get_loader(file_name):
    """get file index loader class from filename

    Args:
        file_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    file_type = get_file_type(file_name)
    if file_type:
        try:
            doc_class = DOCUMENTS[file_type](file_name=file_name)
            return doc_class
        except KeyError:
            print("invalid file type name")
    else:
        print("unrecognized file type")
    return None

def read(filename):
    loader=get_loader(filename)
    return loader.read(filename)


def classify_address(input_string):
    result = {}

    # 正则表达式模式，用于匹配网络地址
    network_pattern = r"^(https?|ftp)://"
    if re.match(network_pattern, input_string):
        # 匹配到了网络地址
        result["type"] = "Network Address"
        protocol_match = re.match(r"^(https?|ftp)://", input_string)
        if protocol_match:
            result["protocol"] = protocol_match.group(1)
        
        # 提取文件名
        file_name = os.path.basename(input_string)
        if file_name:
            result["file_name"] = file_name
            result["file_type"] = os.path.splitext(file_name)[1]

    # 判断是否是网页
    if input_string.startswith("http://") or input_string.startswith("https://"):
        result["type"] = "Web Page"

    # 判断是否是本地目录地址
    if os.path.isdir(input_string):
        result["type"] = "Local Directory"
        
        # 判断操作系统类型
        if os.name == "nt":
            result["system"] = "Windows"
        else:
            result["system"] = "Other"

    # 如果都没有匹配上，则默认为未知类型
    if not result:
        result["type"] = "Unknown"

    return json.dumps(result, indent=4)




# ---------------------------------------------------------------------------- #
#                               ananke data unit                               #
# ---------------------------------------------------------------------------- #


import json
import uuid
from dataclasses import dataclass, field, asdict
from ananke.db.relationdb import SqliteStorage
from ananke.base import BaseModule
def generate_uuid():
    return str(uuid.uuid4())

@dataclass
class Entity:
    id: str = field(default_factory=generate_uuid)
    type: str
    attributes: dict = field(default_factory=dict)
    relations: list = field(default_factory=list)

@dataclass
class LogicExpression:
    id: str = field(default_factory=generate_uuid)
    expression: str
    variables: dict = field(default_factory=dict)

@dataclass
class Symbol:
    id: str = field(default_factory=generate_uuid)
    description: str
    value: float

@dataclass
class MathEquation:
    id: str = field(default_factory=generate_uuid)
    equation: str
    variables: dict = field(default_factory=dict)

@dataclass
class TimeSeriesData:
    id: str = field(default_factory=generate_uuid)
    data: list

@dataclass
class Relationship:
    id: str = field(default_factory=generate_uuid)
    subject_id: str
    object_id: str
    predicate: str

class ananode(BaseModule):
    def __init__(self):
        self.db=SqliteStorage()
        # self.db_name = db_name
        # self.conn = sqlite3.connect(db_name)
        # self.cursor = self.conn.cursor()
        self._initialize_database()

    def _initialize_database(self):
        # 创建表格
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS entities (
                                id TEXT PRIMARY KEY,
                                type TEXT,
                                attributes TEXT,
                                relations TEXT
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS logic_expressions (
                                id TEXT PRIMARY KEY,
                                expression TEXT,
                                variables TEXT
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS symbols (
                                id TEXT PRIMARY KEY,
                                description TEXT,
                                value REAL
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS math_equations (
                                id TEXT PRIMARY KEY,
                                equation TEXT,
                                variables TEXT
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS time_series_data (
                                id TEXT PRIMARY KEY,
                                data TEXT
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS relationships (
                                id TEXT PRIMARY KEY,
                                subject_id TEXT,
                                object_id TEXT,
                                predicate TEXT
                            )''')
        self.conn.commit()

    def _json_encode(self, data):
        return json.dumps(data)

    def _json_decode(self, data):
        return json.loads(data)

    def create_entity(self, entity):
        entity_json = self._json_encode(asdict(entity))
        self.cursor.execute("INSERT INTO entities (id, type, attributes, relations) VALUES (?, ?, ?, ?)",
                            (entity.id, entity.type, entity_json, entity_json))
        self.conn.commit()

    def create_logic_expression(self, logic_expr):
        logic_expr_json = self._json_encode(asdict(logic_expr))
        self.cursor.execute("INSERT INTO logic_expressions (id, expression, variables) VALUES (?, ?, ?)",
                            (logic_expr.id, logic_expr.expression, logic_expr_json))
        self.conn.commit()

    def create_symbol(self, symbol):
        symbol_json = self._json_encode(asdict(symbol))
        self.cursor.execute("INSERT INTO symbols (id, description, value) VALUES (?, ?, ?)",
                            (symbol.id, symbol.description, symbol.value))
        self.conn.commit()

    def create_math_equation(self, math_eq):
        math_eq_json = self._json_encode(asdict(math_eq))
        self.cursor.execute("INSERT INTO math_equations (id, equation, variables) VALUES (?, ?, ?)",
                            (math_eq.id, math_eq.equation, math_eq_json))
        self.conn.commit()

    def create_time_series_data(self, ts_data):
        ts_data_json = self._json_encode(asdict(ts_data))
        self.cursor.execute("INSERT INTO time_series_data (id, data) VALUES (?, ?)",
                            (ts_data.id, ts_data_json))
        self.conn.commit()

    def create_relationship(self, relationship):
        relationship_json = self._json_encode(asdict(relationship))
        self.cursor.execute("INSERT INTO relationships (id, subject_id, object_id, predicate) VALUES (?, ?, ?, ?)",
                            (relationship.id, relationship.subject_id, relationship.object_id, relationship.predicate))
        self.conn.commit()

    def retrieve_entity(self, entity_id):
        self.cursor.execute("SELECT * FROM entities WHERE id=?", (entity_id,))
        row = self.cursor.fetchone()
        if row:
            entity_dict = self._json_decode(row[2])
            return Entity(entity_id, **entity_dict)
        else:
            return None

    def retrieve_relationships(self, subject_id):
        self.cursor.execute("SELECT * FROM relationships WHERE subject_id=?", (subject_id,))
        rows = self.cursor.fetchall()
        relationships = []
        for row in rows:
            relationship_dict = self._json_decode(row[4])
            relationships.append(Relationship(row[0], row[1], row[2], row[3], **relationship_dict))
        return relationships

    def close(self):
        self.conn.close()

