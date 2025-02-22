"""
Script to collect the last 100 Street Fighter 6 match data and save them.

BEFORE RUNNING THIS SCRIPT: We must configure the headers.json file and also retrieve the player short ID
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

Data columns: 

    main_player_name - str - Main player user name
    main_player_sid - int - Main player short id
    main_player_character - str - Main player character name
    main_player_score - int - Main player round won
    main_player_league_rank - int - Main player leagure rank (36 => Master Rank)
    main_player_lp - int - Main player LP during the match
    main_player_mr_ranking - int - Main player world ranking
    main_player_mr - int - Main player MR during the match
    main_player_input_type - int - Main player input type (0 for (C) and 1 for [M])
    main_player_platform - str - Main player platform name

    opposite_player_name - str - Opposite player user name
    opposite_player_sid - int - Opposite player short id
    opposite_player_character - str - Opposite player character name
    opposite_player_score - int - Opposite player round won
    opposite_player_league_rank - int - Opposite player leagure rank (36 => Master Rank)
    opposite_player_lp - int - Opposite player LP during the match
    opposite_player_mr_ranking - int - Opposite player world ranking
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
import copy

import requests
import pandas as pd
import tqdm


# Player short id
PLAYER_SID: int = 1572500566 # MDZ_Jimmy
# PLAYER_SID: int = 3570388222 # Broski

def scrapp_sf6_matches(player_sid: int) -> None:
  # Save file paths
  # csv_file = f"player_{PLAYER_SID}_sf6_matches.csv"
  excel_file: str = f"player_{player_sid}_sf6_matches.xlsx"

  # Ask close files
  if os.path.exists(excel_file):
      input(f"This script will save on {repr(excel_file)} file. Make sure it is closed and press ENTER to proceed.\n")

  # HTTPS request setup
  base_url: str = f"https://www.streetfighter.com/6/buckler/_next/data/gx8EV1nUmBUeAOVLtM_qu/en/profile/{player_sid}/battlelog.json"

  # Retrieve headers
  with open("headers.json") as f:
      headers: dict = json.load(f)

  # Data collection initialization
  match_results: dict = {
      "main_player_name": [],
      "main_player_sid": [],
      "main_player_character": [],
      "main_player_score": [],
      "main_player_league_rank": [],
      "main_player_lp": [],
      "main_player_mr": [],
      "main_player_mr_ranking": [],
      "main_player_input_type": [],
      "main_player_platform": [],

      "opposite_player_name": [],
      "opposite_player_sid": [],
      "opposite_player_character": [],
      "opposite_player_score": [],
      "opposite_player_league_rank": [],
      "opposite_player_lp": [],
      "opposite_player_mr": [],
      "opposite_player_mr_ranking": [],
      "opposite_player_input_type": [],
      "opposite_player_platform": [],

      "match_won": [],
      "left_side": [],
      "uploaded_at": [],
      "replay_id": [],
      "replay_battle_type_name": []
  }

  match_results_template: dict = copy.deepcopy(match_results)

  print("Fetching the last 100 matches...")
  # Data fetching: Can only fetch the last 100 matches through 10 pages.
  with requests.Session() as session:
    for page in tqdm.tqdm(range(1, 11)):

        # Fetch page data
        response: requests.Response = session.get(
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

            left_side: bool = player_1["player"]["short_id"] == player_sid

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

            main_player_mr: int = main_player.get("master_rating", None)
            opposite_player_mr: int = opposite_player.get("master_rating", None)

            main_player_lp: int = main_player.get("league_point", None)
            opposite_player_lp: int = opposite_player.get("league_point", None)

            main_player_mr_ranking: int = main_player.get("master_rating_ranking", None)
            opposite_player_mr_ranking: int = main_player.get("master_rating_ranking", None)

            main_player_league_rank: int = main_player.get("league_rank", None)
            opposite_player_league_rank: int = main_player.get("league_rank", None)
            
            match_won: bool = main_player_score > opposite_player_score

            match_results["main_player_name"].append(main_player_name)
            match_results["main_player_sid"].append(main_player_sid)
            match_results["main_player_character"].append(main_player_character)
            match_results["main_player_score"].append(main_player_score)
            match_results["main_player_mr"].append(main_player_mr)
            match_results["main_player_lp"].append(main_player_lp)
            match_results["main_player_input_type"].append(main_player_input_type)
            match_results["main_player_platform"].append(main_player_platform)
            match_results["main_player_mr_ranking"].append(main_player_mr_ranking)
            match_results["main_player_league_rank"].append(main_player_league_rank)

            match_results["opposite_player_name"].append(opposite_player_name)
            match_results["opposite_player_sid"].append(opposite_player_sid)
            match_results["opposite_player_character"].append(opposite_player_character)
            match_results["opposite_player_score"].append(opposite_player_score)
            match_results["opposite_player_mr"].append(opposite_player_mr)
            match_results["opposite_player_lp"].append(opposite_player_lp)
            match_results["opposite_player_input_type"].append(opposite_player_input_type)
            match_results["opposite_player_platform"].append(opposite_player_platform)
            match_results["opposite_player_mr_ranking"].append(opposite_player_mr_ranking)
            match_results["opposite_player_league_rank"].append(opposite_player_league_rank)

            match_results["match_won"].append(int(match_won))
            match_results["left_side"].append(int(left_side))
            match_results["uploaded_at"].append(replay["uploaded_at"])
            match_results["replay_id"].append(replay["replay_id"])
            match_results["replay_battle_type_name"].append(replay["replay_battle_type_name"])

  df_matches: pd.DataFrame = pd.DataFrame(match_results)

  # Convert match date into a readable timestamp
  df_matches["uploaded_at"] = df_matches["uploaded_at"].map(datetime.datetime.fromtimestamp)

  # Concat with old data if it exists
  old_matches: pd.DataFrame = pd.read_excel(excel_file) if (os.path.exists(excel_file)) else pd.DataFrame(match_results_template)

  df_matches = pd.concat([old_matches, df_matches])

  # Remove duplicate in case of overlapping matches with old data + sort by descending match date
  df_matches = df_matches.drop_duplicates().sort_values("uploaded_at", ascending=False)

  new_match_retrieved: int = len(df_matches) - len(old_matches)

  # Save data into a xlsx file
  df_matches.to_excel(
      excel_file,
      index=False
  )

  print(
    f"\nTotal of {new_match_retrieved} new matche(s) retrieved.\n{len(df_matches)} matches are now saved in {repr(excel_file)} file.\n"
  )

if __name__ == "__main__":
    scrapp_sf6_matches(PLAYER_SID)

