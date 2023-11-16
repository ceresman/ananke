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
import pytest
__author__ = "OOXXXXOO"
__copyright__ = "OOXXXXOO"
__license__ = "MIT"

def test_basic_data():
    pass
    # data=read("example/data/gpt3.pdf")

    # kg_manager = ananode()

    # # 创建实体 - Albert Einstein
    # einstein = Entity(type="Person", attributes={"name": "Albert Einstein"}, relations=[])
    # kg_manager.create_entity(einstein)

    # # 创建逻辑表达式 - Theory of Relativity
    # relativity = LogicExpression(expression="Theory of Relativity", variables={"description": "General and Special Relativity"})
    # kg_manager.create_logic_expression(relativity)

    # # 创建数学关系 - E=mc^2
    # emc2_eq = MathEquation(equation="E=mc^2", variables={"E": "Energy", "m": "Mass", "c": "Speed of Light"})
    # kg_manager.create_math_equation(emc2_eq)

    # # 创建关系 - Einstein's Theory of Relativity includes E=mc^2
    # einstein_relativity_relationship = Relationship(subject_id=einstein.id, object_id=relativity.id, predicate="includes")
    # kg_manager.create_relationship(einstein_relativity_relationship)

    # # 查询实体 - Albert Einstein
    # retrieved_entity = kg_manager.retrieve_entity(einstein.id)
    # print("Retrieved Entity:")
    # print(retrieved_entity)

    # # 查询关系 - Einstein's Theory of Relativity includes E=mc^2
    # relationships = kg_manager.retrieve_relationships(einstein.id)
    # print("Retrieved Relationships:")
    # for relationship in relationships:
    #     print(relationship.__dict__)

    # # 关闭数据库连接
    # kg_manager.close()
