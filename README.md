# Street Fighter 6 History Matches

## Requierment

These scripts use external libraries. They are in the requierment.txt file.
Use this command to install all of them.

```cmd
pip install -r requierment.txt
```

## Data collection script

sf6_match_collection.py script collect the last 100 Street Fighter 6 match data and save them.

**BEFORE RUNNING THIS SCRIPT**: We must configure the headers.json file and also retrieve the player short ID
to make it work:

- Go to the player profile page in https://www.streetfighter.com/6/buckler. 

- Get the 'User Code' for the PLAYER_SID variable.

The following steps should be done once to configure the headers.json file so the https request works.
These steps are done using the Chrome browser but it can normally be done in any other web browser:

- In the player profile, go into the history tab to see all of your history matches.

- Inspect the page (F12) and go to 
  the 'Network' tab (next to 'Elements', 'Console', 'Sources'. It can be found in '>>')
  
- In the main page scroll down to see the paging section and 
  clear the network log (Ctrl + L) to make it easier for the next step.

- Go to another page: A request named 'battlelog.json?page=...' should appear. 
  Click on it to open the header informations.

- In the 'Request Headers' section, copy the whole Cookie value and paste it 
  into the 'Cookie' key in headers.json file. Same for 'User-Agent'.

If the steps are done well you can normally run the script. It will collect data and save them into a
xlsx (excel) file (Make sure to close it if it exists). 
If the file already exists it will add all the new collected matches in it 
while removing duplicates.

#### Data columns: 

- main_player_name - str - Main player user name
- main_player_sid - int - Main player short id
- main_player_character - str - Main player character name
- main_player_score - int - Main player round won
- main_player_mr - int - Main player MR during the match
- main_player_input_type - int - Main player input type (0 for (C) and 1 for [M])
- main_player_platform - str - Main player platform name

- opposite_player_name - str - Opposite player user name
- opposite_player_sid - int - Opposite player short id
- opposite_player_character - str - Opposite player character name
- opposite_player_score - int - Opposite player round won
- opposite_player_mr - int - Opposite player MR during the match
- opposite_player_input_type - Opposite - Main player input type (0 for (C) and 1 for [M])
- opposite_player_platform - Opposite - Main player platform name

- match_won - int - Main player won the match (1 for won and 0 for lost)
- left_side - int - Main player is on the left side (0 for right side and 1 for left side)
- uploaded_at - Timestamp - Timestamp of the match
- replay_id - str - Replay ID
- replay_battle_type_name - str - Match type (Ranked Match, Custom Room ...)

This script doesn't manage data schema changes!

### Data analysis notebook

sf6_match_analysis.ipynb notebook is an example of sf6 matche data analysis code
