"""
Script to collect the last 100 Street Fighter 6 match data and save them.

BEFORE RUNNING THIS SCRIPT: We must retrieve user agent and cookie information to access
battle data and make the script work:

- Go to the player profile page in https://www.streetfighter.com/6/buckler. 

- Get the 'User Code' for the PLAYER_SID variable.

The following steps should be done once to setup the right requst headers so the https request works.
These steps are done using the Chrome browser but it can normally be done in any other web browser:

- In the player profile, go into the history tab to see all of your history matches.

- Inspect the page (F12) and go to 
  the 'Network' tab (next to 'Elements', 'Console', 'Sources'. It can be found in '>>')
  
- In the main page scroll down to see the paging section and 
  clear the network log (Ctrl + L) to make it easier for the next step.

- Go to another page: A request named 'battlelog.json?page=...' should appear. 
  Click on it to open the header informations.

- In the 'Request Headers' section, copy the whole Cookie value and paste it 
  into the 'COOKIE' variable in the script. Same for User-Agent.

If the steps are done well you can normally run the script. It will collect data and save them into a
xlsx (excel) file (Make sure to close it if it exists). 
If the file already exists it will add all the new collected matches in it 
while removing duplicates.

Data columns: 

    main_player_name - str - Main player user name
    main_player_sid - int - Main player short id
    main_player_character - str - Main player character name
    main_player_score - int - Main player round won
    main_player_mr - int - Main player MR during the match
    main_player_input_type - int - Main player input type (0 for (C) and 1 for [M])
    main_player_platform - str - Main player platform name

    opposite_player_name - str - Opposite player user name
    opposite_player_sid - int - Opposite player short id
    opposite_player_character - str - Opposite player character name
    opposite_player_score - int - Opposite player round won
    opposite_player_mr - int - Opposite player MR during the match
    opposite_player_input_type - Opposite - Main player input type (0 for (C) and 1 for [M])
    opposite_player_platform - Opposite - Main player platform name

    match_won - int - Main player won the match (1 for won and 0 for lost)
    left_side - int - Main player is on the left side (0 for right side and 1 for left side)
    uploaded_at - Timestamp - Timestamp of the match
    replay_id - str - Replay ID
    replay_battle_type_name - str - Match type (Ranked Match, Custom Room ...)

This script doesn't manage data schema changes!

"""

import os
import json
import datetime

import requests
import pandas as pd
import tqdm

# Header params
USER_AGENT = "<Paste User Agent Here>"
COOKIE = "<Paste Cookie Here>"

# Player short id
PLAYER_SID: int = 1572500566 # MDZ_Jimmy

# Save file paths
# csv_file = f"player_{PLAYER_SID}_sf6_matches.csv"
excel_file = f"player_{PLAYER_SID}_sf6_matches.xlsx"

# Ask close files
input(f"This script will save on {repr(excel_file)} file. If it exists, make sure it is closed and press ENTER to proceed.\n")

# HTTPS request setup
base_url = f"https://www.streetfighter.com/6/buckler/_next/data/5Qf16SWkd2SZoNO6yXdEg/en/profile/{PLAYER_SID}/battlelog.json"

headers = {
    "User-Agent": USER_AGENT,
    "Cookie": COOKIE,
}

# Data collection initialization
match_results = {
    "main_player_name": [],
    "main_player_sid": [],
    "main_player_character": [],
    "main_player_score": [],
    "main_player_mr": [],
    "main_player_input_type": [],
    "main_player_platform": [],

    "opposite_player_name": [],
    "opposite_player_sid": [],
    "opposite_player_character": [],
    "opposite_player_score": [],
    "opposite_player_mr": [],
    "opposite_player_input_type": [],
    "opposite_player_platform": [],

    "match_won": [],
    "left_side": [],
    "uploaded_at": [],
    "replay_id": [],
    "replay_battle_type_name": []
}

# Data fetching: Can only fetch the last 100 matches through 10 pages.
for page in tqdm.tqdm(range(1, 11)):

    # Fetch page data
    response: requests.Response = requests.get(
        url=base_url + f"?page={page}",
        headers=headers
    )

    if not response.ok:
        print(f"An error occured while fetching page {page}.")
        print(f"Status error code: {response.status_code}.", end="\n\n")
        continue
    
    # Parse json 
    content: dict = json.loads(response.content.decode("ascii", errors="ignore").replace("[t]", ""))

    replay_list: list = content["pageProps"]["replay_list"]

    # Loop through the matches data and collect all the relevant informations
    for replay in replay_list:
        player_1: dict = replay["player1_info"]
        player_2: dict = replay["player2_info"]

        left_side: bool = player_1["player"]["short_id"] == PLAYER_SID

        main_player: dict = player_1 if left_side else player_2
        opposite_player: dict = player_2 if left_side else player_1

        main_player_score: int = sum(r > 0 for r in main_player["round_results"])
        opposite_player_score: int = sum(r > 0 for r in opposite_player["round_results"])

        main_player_name: str = main_player["player"]["fighter_id"]
        opposite_player_name:str = opposite_player["player"]["fighter_id"]

        main_player_sid: str = main_player["player"]["short_id"]
        opposite_player_sid:str = opposite_player["player"]["short_id"]

        main_player_character: str = main_player["character_name"]
        opposite_player_character: str = opposite_player["character_name"]

        main_player_input_type: str = main_player["battle_input_type"]
        opposite_player_input_type: str = opposite_player["battle_input_type"]

        main_player_platform: str = main_player["player"]["platform_name"]
        opposite_player_platform: str = opposite_player["player"]["platform_name"]

        main_player_mr: int = main_player["master_rating"]
        opposite_player_mr: int = opposite_player["master_rating"]

        match_won: bool = main_player_score > opposite_player_score

        match_results["main_player_name"].append(main_player_name)
        match_results["main_player_sid"].append(main_player_sid)
        match_results["main_player_character"].append(main_player_character)
        match_results["main_player_score"].append(main_player_score)
        match_results["main_player_mr"].append(main_player_mr)
        match_results["main_player_input_type"].append(main_player_input_type)
        match_results["main_player_platform"].append(main_player_platform)

        match_results["opposite_player_name"].append(opposite_player_name)
        match_results["opposite_player_sid"].append(opposite_player_sid)
        match_results["opposite_player_character"].append(opposite_player_character)
        match_results["opposite_player_score"].append(opposite_player_score)
        match_results["opposite_player_mr"].append(opposite_player_mr)
        match_results["opposite_player_input_type"].append(opposite_player_input_type)
        match_results["opposite_player_platform"].append(opposite_player_platform)

        match_results["match_won"].append(int(match_won))
        match_results["left_side"].append(int(left_side))
        match_results["uploaded_at"].append(replay["uploaded_at"])
        match_results["replay_id"].append(replay["replay_id"])
        match_results["replay_battle_type_name"].append(replay["replay_battle_type_name"])



df_matches = pd.DataFrame(match_results)

# Convert match date into a readable timestamp
df_matches["uploaded_at"] = df_matches["uploaded_at"].map(datetime.datetime.fromtimestamp)

# Concat with old data if it exists
if (os.path.exists(excel_file)):
    old_matches: pd.DataFrame = pd.read_excel(excel_file)

    df_matches = pd.concat([old_matches, df_matches])

# Remove duplicate in case of overlapping matches with old data + sort by descending match date
df_matches = df_matches.drop_duplicates().sort_values("uploaded_at", ascending=False)


# Save data into a xlsx file
df_matches.to_excel(
    excel_file,
    index=False
)

print(f"\nTotal of {len(df_matches)} matches are now saved in {repr(excel_file)} file.\n")


