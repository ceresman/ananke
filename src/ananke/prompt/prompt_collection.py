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

# example:
    
# The below text is you need to process
# ```markdown
# The National Aeronautics and Space Administration (NASA /ˈnæsə/) is an independent agency of the U.S. federal government responsible for the civil space program, aeronautics research, and space research. Established in 1958, NASA succeeded the National Advisory Committee for Aeronautics (NACA) to give the U.S. space development effort a distinctly civilian orientation, emphasizing peaceful applications in space science.([4])([5])([6]) NASA has since led most American space exploration, including Project Mercury, Project Gemini, the 1968–1972 Apollo Moon landing missions, the Skylab space station, and the Space Shuttle. NASA currently supports the International Space Station and oversees the development of the Orion spacecraft and the Space Launch System for the crewed lunar Artemis program, the Commercial Crew spacecraft, and the planned Lunar Gateway space station.
# NASA's science is focused on: better understanding Earth through the Earth Observing System;([7]) advancing heliophysics through the efforts of the Science Mission Directorate's Heliophysics Research Program;([8]) exploring bodies throughout the Solar System with advanced robotic spacecraft such as New Horizons and planetary rovers such as Perseverance;([9]) and researching astrophysics topics, such as the Big Bang, through the James Webb Space Telescope, and the Great Observatories and associated programs.([10]) NASA's Launch Services Program provides oversight of launch operations and countdown management for its uncrewed launches.
# ```

# Sure, here's the extracted information from the provided data in the format of nodes and relationships:

# Nodes:
# ```json
# [
#   ["nasa", "Organization", {"name": "National Aeronautics and Space Administration"}],
#   ["civil_space_program", "Program", {"name": "Civil Space Program"}],
#   ["aeronautics_research", "Program", {"name": "Aeronautics Research"}],
#   ["space_research", "Program", {"name": "Space Research"}],
#   ["naca", "Organization", {"name": "National Advisory Committee for Aeronautics"}],
#   ["space_development_effort", "Effort", {"name": "Space Development Effort"}],
#   ["space_science", "Field", {"name": "Space Science"}],
#   ["project_mercury", "Project", {"name": "Project Mercury"}],
#   ["project_gemini", "Project", {"name": "Project Gemini"}],
#   ["apollo_moon_missions", "Missions", {"name": "Apollo Moon Landing Missions", "years": "1968–1972"}],
#   ["skylab", "Space Station", {"name": "Skylab"}],
#   ["space_shuttle", "Spacecraft", {"name": "Space Shuttle"}],
#   ["international_space_station", "Space Station", {"name": "International Space Station"}],
#   ["orion_spacecraft", "Spacecraft", {"name": "Orion Spacecraft"}],
#   ["space_launch_system", "Spacecraft", {"name": "Space Launch System"}],
#   ["crewed_lunar_artemis_program", "Program", {"name": "Crewed Lunar Artemis Program"}],
#   ["commercial_crew_spacecraft", "Spacecraft", {"name": "Commercial Crew Spacecraft"}],
#   ["lunar_gateway", "Space Station", {"name": "Lunar Gateway"}],
#   ["earth_observing_system", "Program", {"name": "Earth Observing System"}],
#   ["heliophysics_research", "Program", {"name": "Heliophysics Research Program"}],
#   ["new_horizons", "Spacecraft", {"name": "New Horizons"}],
#   ["perseverance_rover", "Rover", {"name": "Perseverance Rover"}],
#   ["james_webb_telescope", "Telescope", {"name": "James Webb Space Telescope"}],
#   ["great_observatories", "Program", {"name": "Great Observatories"}],
#   ["launch_services_program", "Program", {"name": "Launch Services Program"}]
# ]
# ```

# Relationships:
# ```json
# [
#   ["nasa", "has_program", "civil_space_program", {}],
#   ["nasa", "has_program", "aeronautics_research", {}],
#   ["nasa", "has_program", "space_research", {}],
#   ["nasa", "succeeded", "naca", {"year": 1958}],
#   ["nasa", "focuses_on", "space_science", {}],
#   ["nasa", "led", "project_mercury", {}],
#   ["nasa", "led", "project_gemini", {}],
#   ["nasa", "led", "apollo_moon_missions", {}],
#   ["nasa", "led", "skylab", {}],
#   ["nasa", "led", "space_shuttle", {}],
#   ["nasa", "supports", "international_space_station", {}],
#   ["nasa", "oversees_development_of", "orion_spacecraft", {}],
#   ["nasa", "oversees_development_of", "space_launch_system", {}],
#   ["nasa", "oversees_development_of", "commercial_crew_spacecraft", {}],
#   ["nasa", "oversees_development_of", "lunar_gateway", {}],
#   ["nasa", "focuses_on", "earth_observing_system", {}],
#   ["nasa", "advances_heliophysics_through", "heliophysics_research", {}],
#   ["nasa", "explores_bodies_with", "new_horizons", {}],
#   ["nasa", "explores_bodies_with", "perseverance_rover", {}],
#   ["nasa", "researches_astrophysics_with", "james_webb_telescope", {}],
#   ["nasa", "researches_astrophysics_with", "great_observatories", {}],
#   ["nasa", "provides_oversight_for", "launch_services_program", {}]
# ]
# ```

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

# ---------------------------------- example --------------------------------- #
# The below data is you need process:
# ```
# Nodes:
# ```
# ["nasa", "Organization", {"name": "National Aeronautics and Space Administration", "abbreviation": "NASA"}],
# ["naca", "Organization", {"name": "National Advisory Committee for Aeronautics", "abbreviation": "NACA"}],
# ["civil_space_program", "Program", {"name": "Civil Space Program"}],
# ["aeronautics_research", "Program", {"name": "Aeronautics Research"}],
# ["space_research", "Program", {"name": "Space Research"}],
# ["project_mercury", "Project", {"name": "Project Mercury"}],
# ["project_gemini", "Project", {"name": "Project Gemini"}],
# ["bpolo_moon_landing", "Mission", {"name": "1968–1972 BPOLO Moon landing missions"}],
# ["skylab", "Space Station", {"name": "Skylab"}],
# ["space_shuttle", "Spacecraft", {"name": "Space Shuttle"}],
# ["international_space_station", "Space Station", {"name": "International Space Station"}],
# ["orion_spacecraft", "Spacecraft", {"name": "Orion spacecraft"}],
# ["space_launch_system", "Spacecraft", {"name": "Space Launch System"}],
# ["crewed_lunar_artemis_program", "Program", {"name": "Crewed Lunar Artemis Program"}],
# ["commercial_crew_spacecraft", "Spacecraft", {"name": "Commercial Crew spacecraft"}],
# ["lunar_gateway_space_station", "Space Station", {"name": "Lunar Gateway space station"}],
# ["earth_observing_system", "Program", {"name": "Earth Observing System"}],
# ["heliophysics_research_program", "Program", {"name": "Heliophysics Research Program"}],
# ["new_horizons", "Spacecraft", {"name": "New Horizons"}],
# ["perseverance", "Rover", {"name": "Perseverance"}],
# ["james_webb_space_telescope", "Spacecraft", {"name": "James Webb Space Telescope"}],
# ["great_observatories", "Program", {"name": "Great Observatories"}],
# ```
# Relationships:
# ```
# ["nasa", "succeeded_by", "naca", {}],
# ["nasa", "manages", "civil_space_program", {}],
# ["nasa", "manages", "aeronautics_research", {}],
# ["nasa", "manages", "space_research", {}],
# ["nasa", "led", "project_mercury", {}],
# ["nasa", "led", "project_gemini", {}],
# ["nasa", "led", "bpolo_moon_landing", {}],
# ["nasa", "led", "skylab", {}],
# ["nasa", "led", "space_shuttle", {}],
# ["nasa", "supports", "international_space_station", {}],
# ["nasa", "oversees", "orion_spacecraft", {}],
# ["nasa", "oversees", "space_launch_system", {}],
# ["nasa", "oversees", "crewed_lunar_artemis_program", {}],
# ["nasa", "supports", "commercial_crew_spacecraft", {}],
# ["nasa", "supports", "lunar_gateway_space_station", {}],
# ["nasa", "focuses_on", "earth_observing_system", {}],
# ["nasa", "focuses_on", "heliophysics_research_program", {}],
# ["nasa", "explores_with", "new_horizons", {}],
# ["nasa", "explores_with", "perseverance", {}],
# ["nasa", "researches", "james_webb_space_telescope", {}],
# ["nasa", "researches", "great_observatories", {}],
# ```
# questions or sentences:
# ```
# What kind of spacecraft that NASA build?
# ```
# ```

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

# Here is an example:
# Nodes:
# ```json
# ["luna", "Person", {"name": "Luna"}],
# ["cassie", "Person", {"name": "Cassie"}],
# ```
# Relationships:
# ```json
# ["luna", "is_wife_of", "cassie", {}],
# ["cassie", "is_brother_of", "luna", {}],
# ["luna", "is_stepsister_of", "cassie", {}],
# ```
# Question:
# ```
# What should Luna call Cassie?
# ```
# result:
# ```
# stepbrother
# ```
# Here end of the example.

# Now the default graph I have given:
# Nodes：
# ```
# ["bpolo_moon_landing", "Mission", {"name": "1968–1972 BPOLO Moon landing missions"}],
# ```
# Relations：
# ```
# ["nasa", "led", "bpolo_moon_landing", {}],
# ```
# If you understand the mission, tell me you are ready.




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
