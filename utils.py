import pandas as pd
import numpy as np

def mean_excluding_outliers(series):
    # Calculate the first and third quartile
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    
    # Calculate the interquartile range (IQR)
    iqr = q3 - q1
    
    # Define the lower and upper bound for outliers
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    # Filter out the outliers
    filtered_series = series[(series >= lower_bound) & (series <= upper_bound)]
    
    # Calculate the mean of the filtered series
    mean = filtered_series.mean()
    
    return mean

def find_players_similar_3PCT(pct, three_pct_data):
    player_names = []
    player_name_column = three_pct_data.columns[0]
    three_pct_column = three_pct_data.columns[1]
    for index, row in three_pct_data.iterrows():
        if np.absolute(row[three_pct_column] - pct) < 0.05:
            player_names.append(row[player_name_column])
    
    return player_names