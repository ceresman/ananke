# Prompt Design


## Usage
以下是这个类的使用案例，每个案例都覆盖了不同的函数：

```python
# Import the Prompt class
from your_module import Prompt

# Create an instance of the Prompt class with templates
init_template = "Initialize the system with mode: {mode}"
forward_template = "Perform action: {action} in mode: {mode}"
my_prompt = Prompt(init_template, forward_template)

# Define keyword arguments
init_args = {"mode": "safe"}
forward_args = {"action": "start", "mode": "normal"}

# Example 1: Set the templates and validate_parameters
my_prompt.set_template(init_template, forward_template)

# Example 2: Format an initialization prompt
init_prompt = my_prompt.init(**init_args)
print("Initialization Prompt:", init_prompt)

# Example 3: Format a forward prompt
forward_prompt = my_prompt.forward(**forward_args)
print("Forward Prompt:", forward_prompt)

# Example 4: Call the Prompt instance to generate a forward prompt
forward_prompt = my_prompt(**forward_args)
print("Forward Prompt (via __call__):", forward_prompt)
```

In this example:

1. We create an instance of the `Prompt` class with initialization and forward templates.
2. We define keyword arguments for both initialization and forward prompts.
3. We demonstrate setting templates using `set_template` method.
4. We format an initialization prompt using the `init` method.
5. We format a forward prompt using the `forward` method.
6. We also call the `Prompt` instance as a function to generate a forward prompt, which internally uses the `forward` method.

These examples cover the usage of each function in the `Prompt` class.


## prompt example:
    
The below text is you need to process
```markdown
The National Aeronautics and Space Administration (NASA /ˈnæsə/) is an independent agency of the U.S. federal government responsible for the civil space program, aeronautics research, and space research. Established in 1958, NASA succeeded the National Advisory Committee for Aeronautics (NACA) to give the U.S. space development effort a distinctly civilian orientation, emphasizing peaceful applications in space science.([4])([5])([6]) NASA has since led most American space exploration, including Project Mercury, Project Gemini, the 1968–1972 Apollo Moon landing missions, the Skylab space station, and the Space Shuttle. NASA currently supports the International Space Station and oversees the development of the Orion spacecraft and the Space Launch System for the crewed lunar Artemis program, the Commercial Crew spacecraft, and the planned Lunar Gateway space station.
NASA's science is focused on: better understanding Earth through the Earth Observing System;([7]) advancing heliophysics through the efforts of the Science Mission Directorate's Heliophysics Research Program;([8]) exploring bodies throughout the Solar System with advanced robotic spacecraft such as New Horizons and planetary rovers such as Perseverance;([9]) and researching astrophysics topics, such as the Big Bang, through the James Webb Space Telescope, and the Great Observatories and associated programs.([10]) NASA's Launch Services Program provides oversight of launch operations and countdown management for its uncrewed launches.
```

Sure, here's the extracted information from the provided data in the format of nodes and relationships:

Nodes:
```json
[
  ["nasa", "Organization", {"name": "National Aeronautics and Space Administration"}],
  ["civil_space_program", "Program", {"name": "Civil Space Program"}],
  ["aeronautics_research", "Program", {"name": "Aeronautics Research"}],
  ["space_research", "Program", {"name": "Space Research"}],
  ["naca", "Organization", {"name": "National Advisory Committee for Aeronautics"}],
  ["space_development_effort", "Effort", {"name": "Space Development Effort"}],
  ["space_science", "Field", {"name": "Space Science"}],
  ["project_mercury", "Project", {"name": "Project Mercury"}],
  ["project_gemini", "Project", {"name": "Project Gemini"}],
  ["apollo_moon_missions", "Missions", {"name": "Apollo Moon Landing Missions", "years": "1968–1972"}],
  ["skylab", "Space Station", {"name": "Skylab"}],
  ["space_shuttle", "Spacecraft", {"name": "Space Shuttle"}],
  ["international_space_station", "Space Station", {"name": "International Space Station"}],
  ["orion_spacecraft", "Spacecraft", {"name": "Orion Spacecraft"}],
  ["space_launch_system", "Spacecraft", {"name": "Space Launch System"}],
  ["crewed_lunar_artemis_program", "Program", {"name": "Crewed Lunar Artemis Program"}],
  ["commercial_crew_spacecraft", "Spacecraft", {"name": "Commercial Crew Spacecraft"}],
  ["lunar_gateway", "Space Station", {"name": "Lunar Gateway"}],
  ["earth_observing_system", "Program", {"name": "Earth Observing System"}],
  ["heliophysics_research", "Program", {"name": "Heliophysics Research Program"}],
  ["new_horizons", "Spacecraft", {"name": "New Horizons"}],
  ["perseverance_rover", "Rover", {"name": "Perseverance Rover"}],
  ["james_webb_telescope", "Telescope", {"name": "James Webb Space Telescope"}],
  ["great_observatories", "Program", {"name": "Great Observatories"}],
  ["launch_services_program", "Program", {"name": "Launch Services Program"}]
]
```

Relationships:
```json
[
  ["nasa", "has_program", "civil_space_program", {}],
  ["nasa", "has_program", "aeronautics_research", {}],
  ["nasa", "has_program", "space_research", {}],
  ["nasa", "succeeded", "naca", {"year": 1958}],
  ["nasa", "focuses_on", "space_science", {}],
  ["nasa", "led", "project_mercury", {}],
  ["nasa", "led", "project_gemini", {}],
  ["nasa", "led", "apollo_moon_missions", {}],
  ["nasa", "led", "skylab", {}],
  ["nasa", "led", "space_shuttle", {}],
  ["nasa", "supports", "international_space_station", {}],
  ["nasa", "oversees_development_of", "orion_spacecraft", {}],
  ["nasa", "oversees_development_of", "space_launch_system", {}],
  ["nasa", "oversees_development_of", "commercial_crew_spacecraft", {}],
  ["nasa", "oversees_development_of", "lunar_gateway", {}],
  ["nasa", "focuses_on", "earth_observing_system", {}],
  ["nasa", "advances_heliophysics_through", "heliophysics_research", {}],
  ["nasa", "explores_bodies_with", "new_horizons", {}],
  ["nasa", "explores_bodies_with", "perseverance_rover", {}],
  ["nasa", "researches_astrophysics_with", "james_webb_telescope", {}],
  ["nasa", "researches_astrophysics_with", "great_observatories", {}],
  ["nasa", "provides_oversight_for", "launch_services_program", {}]
]
```






The below data is you need process:

Nodes:
```json
["nasa", "Organization", {"name": "National Aeronautics and Space Administration", "abbreviation": "NASA"}],
["naca", "Organization", {"name": "National Advisory Committee for Aeronautics", "abbreviation": "NACA"}],
["civil_space_program", "Program", {"name": "Civil Space Program"}],
["aeronautics_research", "Program", {"name": "Aeronautics Research"}],
["space_research", "Program", {"name": "Space Research"}],
["project_mercury", "Project", {"name": "Project Mercury"}],
["project_gemini", "Project", {"name": "Project Gemini"}],
["bpolo_moon_landing", "Mission", {"name": "1968–1972 BPOLO Moon landing missions"}],
["skylab", "Space Station", {"name": "Skylab"}],
["space_shuttle", "Spacecraft", {"name": "Space Shuttle"}],
["international_space_station", "Space Station", {"name": "International Space Station"}],
["orion_spacecraft", "Spacecraft", {"name": "Orion spacecraft"}],
["space_launch_system", "Spacecraft", {"name": "Space Launch System"}],
["crewed_lunar_artemis_program", "Program", {"name": "Crewed Lunar Artemis Program"}],
["commercial_crew_spacecraft", "Spacecraft", {"name": "Commercial Crew spacecraft"}],
["lunar_gateway_space_station", "Space Station", {"name": "Lunar Gateway space station"}],
["earth_observing_system", "Program", {"name": "Earth Observing System"}],
["heliophysics_research_program", "Program", {"name": "Heliophysics Research Program"}],
["new_horizons", "Spacecraft", {"name": "New Horizons"}],
["perseverance", "Rover", {"name": "Perseverance"}],
["james_webb_space_telescope", "Spacecraft", {"name": "James Webb Space Telescope"}],
["great_observatories", "Program", {"name": "Great Observatories"}],
```

Relationships:
```json
["nasa", "succeeded_by", "naca", {}],
["nasa", "manages", "civil_space_program", {}],
["nasa", "manages", "aeronautics_research", {}],
["nasa", "manages", "space_research", {}],
["nasa", "led", "project_mercury", {}],
["nasa", "led", "project_gemini", {}],
["nasa", "led", "bpolo_moon_landing", {}],
["nasa", "led", "skylab", {}],
["nasa", "led", "space_shuttle", {}],
["nasa", "supports", "international_space_station", {}],
["nasa", "oversees", "orion_spacecraft", {}],
["nasa", "oversees", "space_launch_system", {}],
["nasa", "oversees", "crewed_lunar_artemis_program", {}],
["nasa", "supports", "commercial_crew_spacecraft", {}],
["nasa", "supports", "lunar_gateway_space_station", {}],
["nasa", "focuses_on", "earth_observing_system", {}],
["nasa", "focuses_on", "heliophysics_research_program", {}],
["nasa", "explores_with", "new_horizons", {}],
["nasa", "explores_with", "perseverance", {}],
["nasa", "researches", "james_webb_space_telescope", {}],
["nasa", "researches", "great_observatories", {}],
```
questions or sentences:

```text
What kind of spacecraft that NASA build?
```


Here is an example:
Nodes:
```json
["luna", "Person", {"name": "Luna"}],
["cassie", "Person", {"name": "Cassie"}],
```
Relationships:
```json
["luna", "is_wife_of", "cassie", {}],
["cassie", "is_brother_of", "luna", {}],
["luna", "is_stepsister_of", "cassie", {}],
```
Question:
```text
What should Luna call Cassie?
```

result:
```text
stepbrother
```
Here end of the example.

Now the default graph I have given:
Nodes：
```json
["bpolo_moon_landing", "Mission", {"name": "1968–1972 BPOLO Moon landing missions"}],
```
Relations：
```json
["nasa", "led", "bpolo_moon_landing", {}],
```
If you understand the mission, tell me you are ready.

