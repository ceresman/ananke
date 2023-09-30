# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __init__.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Winshare Tom <tanwenxuan@live.com>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/09/29 22:42:10 by Winshare To       #+#    #+#              #
#    Updated: 2023/09/30 09:51:02 by Winshare To      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from typing import Any
from dataclasses import dataclass

from ananke.data.code import CodeDocument
from ananke.data.general import *
from ananke.data.media import *
from ananke.data.structure import *

import re


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
    