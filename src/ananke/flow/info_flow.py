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

from ananke.flow import Flow
from ananke.module.extractor import (
    GraphExtractor,
    LogicalRepresentationExtractor,
    MathRepresentationExtractor,
    VectorEmbeddingExtractor,
    UserIntentExtractor,
)
from ananke.module.task import (
    ContentInteraction,
    FoundationAction,
    DataConference,
    ModularizationGeneration,
)


class UserContextFlow(Flow):
    def __init__(self):
        super().__init__()
        
        G=GraphExtractor()
        L=LogicalRepresentationExtractor()
        M=MathRepresentationExtractor()
        V=VectorEmbeddingExtractor()
        U=UserIntentExtractor()
            
        # 将模块添加到Flow中
        self.add_module(G)
        self.add_module(L)
        self.add_module(M)
        self.add_module(V)
        self.add_module(U)
        
        self.add_edge(G,L)
        self.add_edge(M,V)
        self.add_edge(L,U)
        self.add_edge(V,U)
        
        


class DocContextFlow(Flow):
    def __init__(self):
        super().__init__()

