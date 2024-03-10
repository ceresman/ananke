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
import os,json
from ananke.llm.azure import Azure


entity_prompt = """Your goal is to build a graph database. Your task is to extract information from a given text content and convert it into a graph database.
Provide a set of Nodes in the form [ENTITY_ID, TYPE, PROPERTIES] and a set of relationships in the form [ENTITY_ID_1, RELATIONSHIP, ENTITY_ID_2, PROPERTIES].
It is important that the ENTITY_ID_1 and ENTITY_ID_2 exists as nodes with a matching ENTITY_ID. If you can't pair a relationship with a pair of nodes don't add it.
When you find a node or relationship you want to add try to create a generic TYPE for it that describes the entity you can also think of it as a label.
Here , I give you an example of the task:

Example Text Input:

```markdown
Data: Alice lawyer and is 25 years old and Bob is her roommate since 2001. Bob works as a journalist. Alice owns a the webpage www.alice.com and Bob owns the webpage www.bob.com.
```

Example Nodes & Relationships Output:
{
    "Nodes": ["alice", "Person", {"age": 25, "occupation": "lawyer", "name":"Alice"}], ["bob", "Person", {"occupation": "journalist", "name": "Bob"}], ["alice.com", "Webpage", {"url": "www.alice.com"}], ["bob.com", "Webpage", {"url": "www.bob.com"}],
    "Relationships": ["alice", "roommate", "bob", {"start": 2021}], ["alice", "owns", "alice.com", {}], ["bob", "owns", "bob.com", {}]
}
OK, here is the end of the task example.
please output with the given example json format. If you understand your mission rules , please handle now.
"""

content = """
The below text is you need to process
```markdown
The National Aeronautics and Space Administration (NASA /ˈnæsə/) is an independent agency of the U.S. federal government responsible for the civil space program, aeronautics research, and space research. Established in 1958, NASA succeeded the National Advisory Committee for Aeronautics (NACA) to give the U.S. space development effort a distinctly civilian orientation, emphasizing peaceful applications in space science.([4])([5])([6]) NASA has since led most American space exploration, including Project Mercury, Project Gemini, the 1968–1972 Apollo Moon landing missions, the Skylab space station, and the Space Shuttle. NASA currently supports the International Space Station and oversees the development of the Orion spacecraft and the Space Launch System for the crewed lunar Artemis program, the Commercial Crew spacecraft, and the planned Lunar Gateway space station.
NASA's science is focused on: better understanding Earth through the Earth Observing System;([7]) advancing heliophysics through the efforts of the Science Mission Directorate's Heliophysics Research Program;([8]) exploring bodies throughout the Solar System with advanced robotic spacecraft such as New Horizons and planetary rovers such as Perseverance;([9]) and researching astrophysics topics, such as the Big Bang, through the James Webb Space Telescope, and the Great Observatories and associated programs.([10]) NASA's Launch Services Program provides oversight of launch operations and countdown management for its uncrewed launches.
```"""

api_key = "61bc1aab37364618ae0df70bf5f340dd"
api_version = "2024-02-15-preview"
endpoint = "https://anankeus.openai.azure.com/"
api_chat_model = "Ananke3-1106-US-WEST"
api_embed_model = "AnankeEmbedding-US-WEST"
system_prompt = "You are an AI assistant that helps people find information."
message_text = [{"role": "system", "content": system_prompt}, {"role":"user","content": entity_prompt +content}]

client = Azure(
    api_key= api_key,  #密钥1或者密钥2选一个就行
    api_version= api_version,
    azure_endpoint= endpoint, #设定画面上的，格式如 https://xxxxx.openai.azure.com/
    chat_model_name = api_chat_model, embedding_model_name = api_embed_model
)

result = client.get_entity(entity_prompt + content)
print(result)
print(json.loads(result))

graph_dic = {'Nodes': [['nasa', 'Organization', {'type': 'government agency'}], ['naca', 'Organization', {'type': 'government agency'}], 
            ['project_mercury', 'Project', {'type': 'space exploration'}], ['project_gemini', 'Project', {'type': 'space exploration'}], ['skylab', 'Space Station', {'type': 'space station'}], ['space_shuttle', 'Spacecraft', {'type': 'spacecraft'}], ['international_space_station', 'Space Station', {'type': 'space station'}], ['orion_spacecraft', 'Spacecraft', {'type': 'spacecraft'}], ['space_launch_system', 'Spacecraft', {'type': 'spacecraft'}], ['crewed_lunar_artemis_program', 'Program', {'type': 'space exploration'}], ['commercial_crew_spacecraft', 'Spacecraft', {'type': 'spacecraft'}], ['lunar_gateway_space_station', 'Space Station', {'type': 'space station'}], ['earth_observing_system', 'Science Mission', {'type': 'earth observation'}], ['heliophysics_research_program', 'Science Mission', {'type': 'heliophysics research'}], ['new_horizons', 'Spacecraft', {'type': 'space exploration'}], ['perseverance', 'Rover', {'type': 'planetary rover'}], ['james_webb_space_telescope', 'Space Telescope', {'type': 'space telescope'}], ['nasa_launch_services_program', 'Program', {'type': 'launch operations'}]], 
            'Relationships': [['nasa', 'succeeded_by', 'naca', {'start': 1958}], ['nasa', 'led', 'project_mercury', {'start': 1961, 'end': 1963}], ['nasa', 'led', 'project_gemini', {'start': 1965, 'end': 1966}], ['nasa', 'led', 'apollo_moon_landing_missions', {'start': 1968, 'end': 1972}], ['nasa', 'led', 'skylab', {'start': 1973, 'end': 1979}], ['nasa', 'led', 'space_shuttle', {'start': 1981, 'end': 2011}], ['nasa', 'supports', 'international_space_station', {'start': 2000}], ['nasa', 'oversees_development_of', 'orion_spacecraft', {}], ['nasa', 'oversees_development_of', 'space_launch_system', {}], ['nasa', 'oversees_development_of', 'commercial_crew_spacecraft', {}], ['nasa', 'oversees_development_of', 'lunar_gateway_space_station', {}], ['nasa', 'science_focused_on', 'earth_observing_system', {}], ['nasa', 'science_focused_on', 'heliophysics_research_program', {}], ['nasa', 'science_focused_on', 'new_horizons', {}], ['nasa', 'science_focused_on', 'perseverance', {}], ['nasa', 'science_focused_on', 'james_webb_space_telescope', {}], ['nasa', 'launch_services_provided_by', 'nasa_launch_services_program', {}]]}


