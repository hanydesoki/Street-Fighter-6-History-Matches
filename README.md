# Street Fighter 6 History Matches

This project is a program that build a Street Fighter 6 historization matches for a specific player without an interface so we
can retrieve them in seconds using https requests with the SF6 Buckler hidden API.

**Make sure to setup all the requierment below before running the main script (sf6_match_collection.py)**

The data collected will be stored in an excel file and contains useful informations for each matches like the the round scores,
player side, character used etc... You can check the **sf6_match_analysis.ipynb** analysis notebook to get an example of collected data.
The schema is also explained [below](#data-columns).

## Requierments

### Python libraries
These scripts use external libraries. They are in the requierment.txt file.
Use this command to install all of them.

```shell
pip install -r requierment.txt
```

### Setup and configuration of headers.json file 

**BEFORE RUNNING THE SCRIPT**: We must configure the **headers.json** file and also retrieve the **player short ID**
to make it work:

**Retrieve the player short id**

- Go to the player profile page in https://www.streetfighter.com/6/buckler. 

- Get the 'User Code' and paste it in the 'PLAYER_SID' variable as an integer in **sf6_match_collection.py**.

The following steps should be done once to configure the headers.json file so the https request works.
These steps are done using the Chrome browser but it can normally be done in any other web browser:

- In the player profile, go into the history tab to see all of your history matches.

- Inspect the page (F12) and go to 
  the 'Network' tab (next to 'Elements', 'Console', 'Sources'. It can be found in '>>')
  
- In the main page scroll down to see the paging section and 
  clear the network log (Ctrl + L) to make it easier for the next step.

- Click to another page: A request named 'battlelog.json?page=...' should appear. 
  Click on it to open the header informations.

- In the 'Request Headers' section, copy the whole Cookie value and paste it 
  into the **'Cookie'** key in **headers.json** file. Same for **'User-Agent'**.
  **Don't share the cookie informations to anywone else! It may contains your authentifications.**

<img src="https://github.com/hanydesoki/Street-Fighter-6-History-Matches/blob/main/Screen_and_illustrations/network_headers.PNG"/>

If the steps are done well you can normally run the script. It will collect data and save them into a
xlsx (excel) file **(Make sure to close it if it exists)**. 

**This script doesn't manage data schema changes!**

## Data collection script

**sf6_match_collection.py** script collect the last 100 Street Fighter 6 match data and save them in an excel file. 
It will aslo stacks with older saved matches (without duplicates) to make an historization. 
For example if we already saved 100 matches and we run the script later after doing 5 matches it will add these 5 new matches
in the file while keeping the older ones so we have 105 matches.

To keep track of all of your matches, running this script at the end of each session is the way to go but we can run it more frequently
if we want.

To run it, open a terminal in the script directory and run:
```shell
python sf6_match_collection.py
```
It will ask you to close the excel file if it exists, then press ENTER.

The script will fetch trough 10 pages of matches to retrieve in total 100 matches and save them in an excel file in the same directory.
If the file already exists with old match saved, it will concatenate them with the new ones and remove duplicates.

<img src="https://github.com/hanydesoki/Street-Fighter-6-History-Matches/blob/main/Screen_and_illustrations/script_output_example.PNG"/>

## Data columns: 

**Note**: Main player mean that it is the player that correspond to the provided player short id.

- **main_player_name** - str - Main player user name
- **main_player_sid** - int - Main player short id
- **main_player_character** - str - Main player character name
- **main_player_score** - int - Main player round won
- **main_player_mr** - int - Main player MR during the match
- **main_player_input_type** - int - Main player input type (0 for (C) and 1 for [M])
- **main_player_platform** - str - Main player platform name

- **opposite_player_name** - str - Opposite player user name
- **opposite_player_sid** - int - Opposite player short id
- **opposite_player_character** - str - Opposite player character name
- **opposite_player_score** - int - Opposite player round won
- **opposite_player_mr** - int - Opposite player MR during the match
- **opposite_player_input_type** - Opposite - Main player input type (0 for (C) and 1 for [M])
- **opposite_player_platform** - Opposite - Main player platform name

- **match_won** - int - Main player won the match (1 for won and 0 for lost)
- **left_side** - int - Main player is on the left side (0 for right side and 1 for left side)
- **uploaded_at** - Timestamp - Timestamp of the match
- **replay_id** - str - Replay ID
- **replay_battle_type_name** - str - Match type (Ranked Match, Custom Room ...)

### Data analysis notebook

**sf6_match_analysis.ipynb** notebook is an example of sf6 match data analysis code. It can be runned after collecting the data in the excel file.
