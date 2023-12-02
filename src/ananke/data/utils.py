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
    "PostScriptDocument": r"\.ps$",
    "NetworkAddress": r"^(https?|ftp)://",
    "Unknown": r"^.*$"
}


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


# 定义一个函数，根据文件名获取文件类型
def get_type(file_name):
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


# 定义一个函数，根据文件名获取相应的loader类
def get_loader(file_name):
    """get file index loader class from filename

    Args:
        file_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    file_type = get_type(file_name)
    if file_type:
        try:
            doc_class = DOCUMENTS[file_type](file_name=file_name)
            return doc_class
        except KeyError:
            print("invalid file type name")
    else:
        print("unrecognized file type")
    return None
