import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo
import time

sleep_time = .5

def get_active_players_for_season(season):
    # Get all players
    print("Collecting player info")
    all_players = players.get_players()
    player_info = []
    for p in all_players:
        player_info.append(commonplayerinfo.CommonPlayerInfo(p['id']))
        time.sleep(sleep_time)

    # Filter active players for the specified season
    active_players = [
        player for player in player_info 
        if player['is_active'] and player['from_year'] <= season[:4] <= player['to_year']
    ]

    return active_players


def get_historical_3pt_percentage_for_season(excluded_season):
    # Get all active players from the excluded season
    active_players = get_active_players_for_season(excluded_season)
    # DataFrame to store the results
    player_3pt_stats = pd.DataFrame(columns=['Player', '3P%', 'Seasons'])
    player_names = []
    three_percentages = []
    print("Collecting three point percentages")
    for player in active_players:
        time.sleep(sleep_time)
        # Fetch career statistics for the player
        career = playercareerstats.PlayerCareerStats(player_id=player['id'])
        career_df = career.get_data_frames()[0]

        # Filter out the excluded season
        filtered_df = career_df[career_df['SEASON_ID'] != excluded_season]

        # Calculate total 3-point attempts and made shots
        total_attempts = filtered_df['FG3A'].sum()
        total_made = filtered_df['FG3M'].sum()

        # Calculate 3-point percentage
        three_point_pct = total_made / total_attempts if total_attempts > 0 else 0


    return player_names, three_percentages

def get_player_3p_stats(player_name, season):
    """
    Get the 3-Point Attempts (3PA) and 3-Point Made (3PM) for a given player in a specific season.
    """
    
    # Find player by name
    player_dict = [player for player in players.get_players() if player['full_name'] == player_name]

    if not player_dict:
        raise ValueError("Player not found")

    # Get player ID
    player_id = player_dict[0]['id']

    # Get player career stats
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_df = career.get_data_frames()[0]

    # Filter stats by season
    season_stats = career_df[career_df['SEASON_ID'] == f'2{season}']

    if season_stats.empty:
        return None, None

    # Extract 3PA and 3PM
    three_pa = season_stats['FG3A'].iloc[0]
    three_pm = season_stats['FG3M'].iloc[0]

    return three_pa, three_pm

def collect_season_data(season):
    player_names, three_pct = get_historical_3pt_percentage_for_season(excluded_season=season)
    three_attempts = []
    three_makes = []
    for p in player_names:
        print("Collecting " + player + " 3PA, 3PM")
        time.sleep(sleep_time)
        a, m = get_player_3p_stats(p, season)
        three_attempts.append(a)
        three_makes.append(m)
    
    return pd.DataFrame({"PLAYER":player_names, "3P%": three_pct, "3PM": three_makes, "3PA": three_attempts})

df = collect_season_data("2023-24")
df.to_csv("Data/input/players_2023-24.csv")