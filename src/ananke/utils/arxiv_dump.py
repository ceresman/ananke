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

import os
import zipfile
import uuid
import mysql.connector
import PyPDF2
import textract
import docx
import csv
# import pyeps
import bibtexparser
import subprocess  # 用于运行外部命令
import zipfile
import tarfile  # 引入tarfile模块来处理.tar和.tar.gz文件
from tqdm import tqdm
import gzip  # 引入gzip模块来处理.gz文件
import magic

# 已解压的文件夹路径集合
extracted_folders = set()

def extract_archive(archive_path):
    # 获取文件扩展名
    file_extension = os.path.splitext(archive_path)[1]

    if file_extension == ".zip":
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(archive_path))
    elif file_extension == ".tar":
        with tarfile.open(archive_path, 'r') as tar_ref:
            tar_ref.extractall(os.path.dirname(archive_path))
    elif file_extension == ".tar.gz":
        with tarfile.open(archive_path, 'r:gz') as tar_ref:
            tar_ref.extractall(os.path.dirname(archive_path))
    elif file_extension == ".gz":
        with gzip.open(archive_path, 'rb') as gz_file:
            # 解压后的文件路径
            uncompressed_file_path = os.path.splitext(archive_path)[0]

            # 获取解压后的文件内容
            content = gz_file.read()

            # 使用 magic 模块判断文件类型
            file_type = magic.from_buffer(content, mime=True)
            print("decompress file | "+uncompressed_file_path+" | add type:", file_type)

            # 根据文件类型添加后缀
            uncompressed_file_path += get_file_extension(file_type)

            # 将解压后的内容保存到新的文件
            with open(uncompressed_file_path, 'wb') as output_file:
                output_file.write(content)

    # 获取解压的文件夹路径
    extracted_folder = os.path.splitext(archive_path)[0]

    # 如果解压的文件夹路径不在已解压的文件夹集合中，继续递归处理
    if extracted_folder not in extracted_folders:
        extracted_folders.add(extracted_folder)

        # 处理解压后的文件夹中的文件
        for root, _, files in os.walk(extracted_folder):
            print("process progress : ")
            for file in tqdm(files):
                file_path = os.path.join(root, file)
                # print("processing:", file_path)
                # process_file(file_path)

                # 如果解压的文件是一个压缩文件，递归处理
                if is_archive(file_path):
                    extract_archive(file_path)

# 判断文件是否是压缩文件
def is_archive(file_path):
    return file_path.endswith((".zip", ".tar", ".tar.gz", ".gz"))

# 根据文件类型获取文件后缀
def get_file_extension(file_type):
    # if file_type.startswith("text/"):
        # return ".txt"
    if file_type == "application/pdf":
        return ".pdf"
    elif file_type == "application/vnd.ms-powerpoint":
        return ".ppt"
    elif file_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
        return ".pptx"
    elif file_type == "application/msword":
        return ".doc"
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return ".docx"
    elif file_type == "application/postscript":
        return ".ps"
    elif file_type == "application/x-latex" or file_type == "text/x-tex" or file_type == "text/plain":
        return ".tex"
    # 添加其他常见文档格式的处理
    else:
        return ""



# 处理PDF文件的函数
def process_pdf(file_path):
    with open(file_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        num_pages = pdf_reader.numPages
        text = ""
        for page_num in range(num_pages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
        # 处理PDF文本

# 处理Latex文件的函数
def process_latex(file_path):
    text = textract.process(file_path).decode("utf-8")
    # 处理Latex文本

# 处理Word文档的函数
def process_docx(file_path):
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text
    # 处理Word文档文本

# 处理CSV文件的函数
def process_csv(file_path):
    with open(file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        pass
        # for row in csv_reader:
        #     # 处理CSV数据行

# 处理EPS文件的函数
# def process_eps(file_path):
    # eps_image = pyeps.load(file_path)
    # 处理EPS图像

# 处理BibTeX文件的函数
def process_bibtex(file_path):
    with open(file_path, "r") as bib_file:
        bibtex_database = bibtexparser.load(bib_file)
        # 处理BibTeX数据
# 定义一个函数来处理文件


def process_file(file_path):
    # 获取文件扩展名
    file_extension = os.path.splitext(file_path)[1]
    
    # 处理不同类型的文件
    if file_extension == ".pdf":
        process_pdf(file_path)
    elif file_extension == ".tex":
        process_latex(file_path)
    elif file_extension == ".docx":
        process_docx(file_path)
    elif file_extension == ".csv":
        process_csv(file_path)
    # elif file_extension == ".eps":
        # process_eps(file_path)
    elif file_extension == ".bib":
        process_bibtex(file_path)
    elif file_extension == ".ps":
        # 将.ps文件转换为.pdf
        pdf_file_path = convert_ps_to_pdf(file_path)
        if pdf_file_path:
            process_pdf(pdf_file_path)
    else:
        # 处理其他未知文件类型的逻辑
        pass

    # 获取文件的元信息
    file_meta = {
        "uuid": str(uuid.uuid4()),
        "title": "文件标题",  # 替换为实际的标题
        "author": "作者名",  # 替换为实际的作者
        "keywords": "关键字",  # 替换为实际的关键字
        # 添加其他元信息字段
    }

    # 将元信息写入MariaDB数据库
    # write_to_database(file_meta)

# 处理.ps文件并将其转换为.pdf
def convert_ps_to_pdf(ps_file_path):
    pdf_file_path = os.path.splitext(ps_file_path)[0] + ".pdf"
    try:
        subprocess.run(["gs", "-o", pdf_file_path, "-sDEVICE=pdfwrite", ps_file_path])
        return pdf_file_path
    except Exception as e:
        print(f"Error converting .ps to .pdf: {e}")
        return None

# 其他函数不变...

# 定义一个函数来将文件元信息写入数据库
def write_to_database(file_meta):
    connection = mysql.connector.connect(
        host="数据库主机地址",
        user="数据库用户名",
        password="数据库密码",
        database="数据库名称"
    )

    cursor = connection.cursor()

    insert_query = """
    INSERT INTO documents (uuid, title, author, keywords)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(insert_query, (
        file_meta["uuid"],
        file_meta["title"],
        file_meta["author"],
        file_meta["keywords"]
    ))

    connection.commit()
    cursor.close()
    connection.close()

# 主函数
if __name__ == "__main__":
    root_directory = "/smb/workspace/ARXIV/sample/"  # 替换为实际的根目录路径
    extract_archive(root_directory)
