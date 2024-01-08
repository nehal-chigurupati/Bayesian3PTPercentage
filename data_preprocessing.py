import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo
import time
from sqlalchemy import create_engine

sleep_time = 1

def get_active_player_info():
    # Get all players
    print("Collecting player info")
    all_players = players.get_active_players()
    player_info = []
    counter = 0
    for p in all_players:
        print("Collecting info for player " + str(counter) +"/" + str(len(all_players)))
        counter += 1
        player_info.append(commonplayerinfo.CommonPlayerInfo(p['id']).get_data_frames()[0])
        time.sleep(sleep_time)

    return pd.concat(player_info)

def get_player_career_stats(player_id):
    return playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]

def get_historical_3pt_percentage(career_df):

    # Filter out the current season
    filtered_df = career_df[career_df['SEASON_ID'] != "2023-24"]

    # Calculate total 3-point attempts and made shots
    total_attempts = filtered_df['FG3A'].sum()
    total_made = filtered_df['FG3M'].sum()

    # Calculate 3-point percentage
    three_point_pct = total_made / total_attempts if total_attempts > 0 else 0

    return three_point_pct

def get_player_3p_stats(career_df):
    """
    Get the 3-Point Attempts (3PA) and 3-Point Made (3PM) for a given player in a specific season.
    """

    # Filter stats by season
    season_stats = career_df[career_df['SEASON_ID'] == "2023-24"]

    if season_stats.empty:
        return None, None

    # Extract 3PA and 3PM
    three_pa = season_stats['FG3A'].iloc[0]
    three_pm = season_stats['FG3M'].iloc[0]

    return three_pa, three_pm

engine = create_engine("sqlite:///Data/player_database.db")

"""
#Get players from this season
active_players = get_active_player_info()
active_players.to_sql("COMMON_PLAYER_INFO", con=engine, if_exists="replace", index=False)
"""
"""
#Get player career stats
player_ids = pd.read_sql("COMMON_PLAYER_INFO", engine)["PERSON_ID"].tolist()
counter = 0
dfs = []
for player in player_ids:
    print("Collecting career stats for player " + str(counter)+"/"+str(len(player_ids)))
    counter += 1
    dfs.append(playercareerstats.PlayerCareerStats(player_id=player).get_data_frames()[0])
career_df = pd.concat(dfs)
career_df.to_sql("PLAYER_CAREER_STATS", con=engine, if_exists="replace", index=False)
"""

#Calculate and store 3 pointer data
player_ids = pd.read_sql("COMMON_PLAYER_INFO", engine)["PERSON_ID"].tolist()
career_stats = pd.read_sql("PLAYER_CAREER_STATS", engine)

three_pcts = []
three_pa = []
three_pm = []
counter = 0

for id in player_ids:
    print("Computing 3PT stats for player " + str(counter)+"/"+str(len(player_ids)))
    counter += 1
    player_df = career_stats[career_stats["PLAYER_ID"] == id]
    three_pcts.append(get_historical_3pt_percentage(player_df))
    pa, pm = get_player_3p_stats(player_df)
    three_pa.append(pa)
    three_pm.append(pm)

out_df = pd.DataFrame({"PLAYER_ID": player_ids, "HISTORICAL_3P%": three_pcts, "SEASON_3PA": three_pa, "SEASON_3PM": three_pm})
out_df.to_sql("BAYESIAN_3PT_INPUT_2023_24", con=engine, if_exists="replace", index=False)
