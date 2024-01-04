import pandas as pd
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players

def get_active_players_3p_stats(season='2023-24'):
    # Get all players
    all_players = players.get_active_players()

    # Create an empty DataFrame to store player stats
    player_stats_df = pd.DataFrame(columns=['Player', '3P%', '3PA', '3PM'])

    # Iterate through each player and get their stats
    player_names = []
    three_perc = []
    three_attempts = []
    three_makes = []
    for player in all_players:
        # Fetch game log for the player for the specified season
        gamelog = playergamelog.PlayerGameLog(player_id=player['id'], season=season)

        # Convert to DataFrame
        gamelog_df = gamelog.get_data_frames()[0]

        # Calculate total 3P%, 3PA, and 3PM
        total_3pa = gamelog_df['FG3A'].sum()
        total_3pm = gamelog_df['FG3M'].sum()
        three_point_pct = total_3pm / total_3pa if total_3pa > 0 else 0

        player_names.append(player)
        three_perc.append(three_point_pct)
        three_attempts.append(total_3pa)
        three_makes.append(total_3pm)


    return pd.DataFrame({"PLAYER": player_names, "3P%": three_perc, "3PA": three_attempts, "3PM": three_makes})

get_active_players_3p_stats().to_csv("Data/input/player_data_2023-24.csv")