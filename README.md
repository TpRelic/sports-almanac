# Online Sports Almanac
#### 'Server/Software Project' 

The project is a web application that allows users to directly query professional league metrics and provide an AI analysis agent if the user wants recommendations and feedback on the data.
No user account or information is required, making the process of querying: quick, convenient, simple, and safe!

This project aims to aid in providing definitive facts, stats, and data in an accessible manner.
Using various league APIs and pre-selected datasets, we hope to provide accurate and clear metrics on teams, seasons, players, and more.
In its current state, it is tedious to sift through various APIs and data sources to get clear information on a player or team during the live game.
Through our Online Sports Almanac, we allow the user to skip the annoying search process, ask our application about any given metrics, and keep them informed about the game right as it happens.
Furthermore, the user can use the data we find for them and make inquiries to an AI agent, facilitating a better response than a typical AI or looking at data alone.

## Instructions
pip_installs.bat (should) have the pip installs you need to run the server side.

make sure your environment or .env has a valid gemini api key.

todo, front end / clientside stuff.

## component list (move later)
#### ask_ai.py
does the gemini stuff, calls nba stats, etc
#### check_api_key.py
sees if your env var exists or not
#### example_prompts.py
has plaintext prompts that it makes into a chat history
#### get_nba_stats.py
todo, maybe use a database so we dont ask the nba api all every time (but its fast so its fine)
