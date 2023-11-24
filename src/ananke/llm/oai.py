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
import re
import requests
import sys
from num2words import num2words
import os
import pandas as pd
import numpy as np
import tiktoken
from typing import List
from openai import AzureOpenAI

# ------------------------------------- - ------------------------------------ #
from ananke.llm import RemoteLLM


class AzureOpenAIAssistant(RemoteLLM):
    def __init__(
        self,
        api_key=None,
        api_version=None,
        azure_endpoint=None,
        tokenizer=None,
        max_token=8192,
        system_prompt="You are a helpful assistant.",
    ):
        self.api_key = api_key
        self.api_version = api_version
        self.azure_endpoint = azure_endpoint
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.azure_endpoint,
        )
        self.conversation = [{"role": "system", "content": system_prompt}]
        if tokenizer is None:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.max_token = max_token

    def chat(self, user_input):
        self.conversation.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model="Ananke", messages=self.conversation
        )

        self.conversation.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )

        return response.choices[0].message.content

    def normalize_text(self, s, sep_token="\n "):
        s = re.sub(r"\s+", " ", s).strip()
        s = re.sub(r". ,", "", s)
        s = s.replace("..", ".")
        s = s.replace(". .", ".")
        s = s.replace("\n", "")
        s = s.strip()
        return s

    def embedding(self, text: str, embedding_model="AnankeEmbedding"):
        text = self.normalize_text(text)
        embedding = (
            self.client.embeddings.create(input=[text], model=embedding_model)
            .data[0]
            .embedding
        )
        print(len(embedding))
        return embedding

    def embedding_df(
        self, df: pd.DataFrame, text_column: str, embedding_model="AnankeEmbedding"
    ):  
      """process embedding as dataframe batch

      Args:
          df (pd.DataFrame): _description_
          text_column (str): _description_
          embedding_model (str, optional): _description_. Defaults to "AnankeEmbedding".

      Returns:
          pd.Dataframe: _description_
      """
        df[text_column] = df[text_column].apply(lambda x: self.normalize_text(x))
        df["n_tokens"] = df[text_column].apply(lambda x: len(self.tokenizer.encode(x)))
        df = df[df.n_tokens < self.max_token]
        df[f"{embedding_model}"] = df[text_column].apply(
            lambda x: self.embedding(x, embedding_model=embedding_model)
        )
        return df

    def cosine_similarity(self, a, b):
        """
        Takes 2 vectors a, b and returns the cosine similarity according
        to the definition of the dot product
        """
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def search_docs(self, df: pd.DataFrame, user_query: str, top_n=4):
        user_query_embedding = self.embedding(user_query)
        df["similarities"] = df.AnankeEmbedding.apply(
            lambda x: self.cosine_similarity(x, user_query_embedding)
        )
        print(df)
        res = df.sort_values("similarities", ascending=False).head(top_n)
        return res


# 示例用法

# assistant = AzureOpenAIAssistant(api_key, api_version, azure_endpoint)

# df = pd.DataFrame(
#     {
#         "text": [
#             "NASA traces its roots to the National Advisory Committee for Aeronautics (NACA). ",
#             "Determined to regain American leadership in aviation, Congress created the Aviation Section of the U.S. Army Signal Corps in 1914 and established NACA in 1915 to foster aeronautical research and development.",
#         ]
#     }
# )

# df = assistant.embedding_df(df, "text")


# print(df)

# print(assistant.search_docs(df, "What is nasa root from?"))

#                                                text  n_tokens                                    AnankeEmbedding
# 0  NASA traces its roots to the National Advisory...        18  [-0.001609626691788435, -0.01872904784977436, ...
# 1  Determined to regain American leadership in av...        43  [-0.023721234872937202, -0.02078939788043499, ...
# 1536
#                                                 text  ...  similarities
# 0  NASA traces its roots to the National Advisory...  ...      0.801512
# 1  Determined to regain American leadership in av...  ...      0.745144

# [2 rows x 4 columns]
#                                                 text  ...  similarities
# 0  NASA traces its roots to the National Advisory...  ...      0.801512
# 1  Determined to regain American leadership in av...  ...      0.745144
