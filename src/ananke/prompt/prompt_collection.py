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







# ---------------------------------------------------------------------------- #
#                              REASONING_ARGUMENT                              #
# ---------------------------------------------------------------------------- #













# ---------------------------------------------------------------------------- #
#                               GENERATE_AUGUMENT                              #
# ---------------------------------------------------------------------------- #


# Please note that the relationships and properties mentioned in the example are generic placeholders based on the context of the data provided. You can modify and expand upon them according to your requirements and the actual information you're working with.


CHUNK_TO_KG_GRAPH_INIT = """
Your goal is to build a graph database. Your task is to extract information from a given text content and convert it into a graph database.
Provide a set of Nodes in the form [ENTITY_ID, TYPE, PROPERTIES] and a set of relationships in the form [ENTITY_ID_1, RELATIONSHIP, ENTITY_ID_2, PROPERTIES].
It is important that the ENTITY_ID_1 and ENTITY_ID_2 exists as nodes with a matching ENTITY_ID. If you can't pair a relationship with a pair of nodes don't add it.
When you find a node or relationship you want to add try to create a generic TYPE for it that describes the entity you can also think of it as a label.
Here , I give you an example of the task:

Example Text Input:

```markdown
Data: Alice lawyer and is 25 years old and Bob is her roommate since 2001. Bob works as a journalist. Alice owns a the webpage www.alice.com and Bob owns the webpage www.bob.com.
```

Example Nodes & Relationships Output:

Nodes: 
```json
["alice", "Person", {"age": 25, "occupation": "lawyer", "name":"Alice"}], ["bob", "Person", {"occupation": "journalist", "name": "Bob"}], ["alice.com", "Webpage", {"url": "www.alice.com"}], ["bob.com", "Webpage", {"url": "www.bob.com"}]
```
Relationships: 
```json
["alice", "roommate", "bob", {"start": 2021}], ["alice", "owns", "alice.com", {}], ["bob", "owns", "bob.com", {}] 
```
OK, here is the end of the task example.
please don't forget the output format. If you understand your mission rules , tell me you are ready.

"""


CHUNK_TO_KG_GRAPH_CHAT = """
The below text is you need to process
```markdown
{USER_INPUT}
```
"""



# --------------------------- KG_SENTENCES_RELATED --------------------------- #




KG_SENTENCES_RELATED_INIT = """

You are a data scientist， and the purpose for getting related relationships & nodes from input knowledge with specific questions or sentences. Additionally, you need to generate with example format strictly.
Here is an example:

Nodes:
```
{KG_SENTENCES_RELATED_EXAMPLE_INPUT_NODES}
```
Relationships:
```
{KG_SENTENCES_RELATED_EXAMPLE_INPUT_RELATIONSHIPS}
```
questions or sentences:
```
What did BPOLO Moon landing missions need to do in 1969?
```
result:
```
Nodes:
```
{KG_SENTENCES_RELATED_EXAMPLE_OUTPUT_NODES}
```

Relationships:
```
{KG_SENTENCES_RELATED_EXAMPLE_OUTPUT_RELATIONSHIPS}
```
```

Here is the end of the example, If you understand the mission tell me you are ready.

"""


KG_SENTENCES_RELATED_EXAMPLE_INPUT_NODES = """

["nasa", "Organization", {"name": "National Aeronautics and Space Administration", "abbreviation": "NASA"}],
["naca", "Organization", {"name": "National Advisory Committee for Aeronautics", "abbreviation": "NACA"}],
["civil_space_program", "Program", {"name": "Civil Space Program"}],
["aeronautics_research", "Program", {"name": "Aeronautics Research"}],
["space_research", "Program", {"name": "Space Research"}],
["project_mercury", "Project", {"name": "Project Mercury"}],
["project_gemini", "Project", {"name": "Project Gemini"}],
["bpolo_moon_landing", "Mission", {"name": "1968–1972 BPOLO Moon landing missions"}],
["skylab", "Space Station", {"name": "Skylab"}],

"""

KG_SENTENCES_RELATED_EXAMPLE_INPUT_RELATIONSHIPS = """

["nasa", "succeeded_by", "naca", {}],
["nasa", "manages", "civil_space_program", {}],
["nasa", "manages", "aeronautics_research", {}],
["nasa", "manages", "space_research", {}],
["nasa", "led", "project_mercury", {}],
["nasa", "led", "project_gemini", {}],
["nasa", "led", "bpolo_moon_landing", {}],
["nasa", "led", "skylab", {}],
["nasa", "led", "space_shuttle", {}],

"""

KG_SENTENCES_RELATED_EXAMPLE_OUTPUT_NODES="""
["nasa", "Organization", {"name": "National Aeronautics and Space Administration", "abbreviation": "NASA"}],
["bpolo_moon_landing", "Mission", {"name": "1968–1972 BPOLO Moon landing missions"}],
"""

KG_SENTENCES_RELATED_EXAMPLE_OUTPUT_RELATIONSHIPS="""
["nasa", "led", "bpolo_moon_landing", {}],
"""


KG_SENTENCES_RELATED_FORWARD="""
The below data is you need process:
```
Nodes:
```
{NODES}
```
Relationships:
```
{RELATIONS}
```
questions or sentences:
```
{USER_INPUT}
```
```

"""

# ---------------------------------------------------------------------------- #
#                              CHAT_WITH_KG_ROUND                              #
# ---------------------------------------------------------------------------- #

# In the next chat process， you just can reply with information from the given knowledge graph relationships & nodes:




CHAT_WITH_KG_ROUND = """

In the next chat process， you just can reply with information from the given knowledge graph relationships & nodes:

Here is an example:

Nodes:
```json
{EXAMPLE_KG_NODES}
```
Relationships:
```json
{EXAMPLE_KG_RELATIONSHIPS}
```
Question:
```
What should Luna call Cassie?
```
result:
```
stepbrother
```


Here end of the example.

Now the default graph I have given:

Nodes:
```
{NODES}
```

Relations:
```
{RELATIONS}
```
```

If you understand the mission, tell me you are ready.

"""
EXAMPLE_KG_NODES = """
["luna", "Person", {"name": "Luna"}],
["cassie", "Person", {"name": "Cassie"}],
["mark", "Person", {"name": "Mark"}],
"""
EXAMPLE_KG_RELATIONSHIPS = """
["luna", "is_wife_of", "cassie", {}],
["cassie", "is_brother_of", "mark", {}],
["luna", "is_stepsister_of", "mark", {}],
"""

# Notes: The example nodes & relationships is just for init, you can modify it as you want.

# ------------------------------------- - ------------------------------------ #



# ---------------------------------------------------------------------------- #
#                                  COLLECTION                                  #
# ---------------------------------------------------------------------------- #
COLLECTION = {
    "CHUNK_TO_KG_GRAPH_INIT" : CHUNK_TO_KG_GRAPH_INIT,
    "CHUNK_TO_KG_GRAPH_CHAT" : CHUNK_TO_KG_GRAPH_CHAT,
    "KG_SENTENCES_RELATED_INIT" : KG_SENTENCES_RELATED_INIT,
    "KG_SENTENCES_RELATED_FORWARD" : KG_SENTENCES_RELATED_FORWARD,
    "CHAT_WITH_KG_ROUND" : CHAT_WITH_KG_ROUND,
    "EXAMPLE_KG_NODES" : EXAMPLE_KG_NODES,
    "EXAMPLE_KG_RELATIONSHIPS" : EXAMPLE_KG_RELATIONSHIPS,
    "KG_SENTENCES_RELATED_EXAMPLE_INPUT_NODES" : KG_SENTENCES_RELATED_EXAMPLE_INPUT_NODES,
    "KG_SENTENCES_RELATED_EXAMPLE_INPUT_RELATIONSHIPS" : KG_SENTENCES_RELATED_EXAMPLE_INPUT_RELATIONSHIPS,
    "KG_SENTENCES_RELATED_EXAMPLE_OUTPUT_NODES" : KG_SENTENCES_RELATED_EXAMPLE_OUTPUT_NODES,
    "KG_SENTENCES_RELATED_EXAMPLE_OUTPUT_RELATIONSHIPS" : KG_SENTENCES_RELATED_EXAMPLE_OUTPUT_RELATIONSHIPS
}
