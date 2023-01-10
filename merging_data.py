import pandas as pd
import numpy as np

# loading steam_spy dataframe and changing the 'appid' column to 'app_id' so it can be merged with the steam_reviews dataframe
steamspy = pd.read_csv('./steam_data/data/download/steamspy_data.csv')
steamspy.rename(columns={"appid": "app_id"}, inplace = True)

# loading steam_app_data dataframe and changing the 'steam_appid' column to 'app_id' so it can be merged with the steam_reviews dataframe
steam = pd.read_csv('./steam_data/data/download/steam_app_data.csv')
steam.rename(columns={"steam_appid": "app_id"}, inplace = True)

# deleting the unnecessary and inaccurate columns from the steam_data table and adding useful columns from steam_app_data to it
clean_steam_data = pd.merge(steamspy, steam[['app_id', 'recommendations', 'metacritic']], on='app_id', how='left')
clean_steam_data.drop(['score_rank', 'userscore', 'owners', 'price', 'initialprice', 'discount', 'discount', 'average_2weeks', 'median_2weeks'], axis=1, inplace=True)

# extracting integers from scores and recommendations and dropping the initial column
clean_steam_data['metacritic_score'] = clean_steam_data.metacritic.str.extract('(\d+)')
clean_steam_data['total_recommendations'] = clean_steam_data.recommendations.str.extract('(\d+)')
clean_steam_data.drop(['metacritic', 'recommendations'], axis = 1, inplace = True)

# exporting the cleaned dataframe
clean_steam_data.to_csv('clean_steam_data.csv', index = False)

# loading the steam_reviews dataframe and merging it with the clean dataframe we just created using the 'app_id' column as the main key
reviews = pd.read_csv('./steam_reviews.csv')
merged_data = pd.merge(clean_steam_data, reviews, on = 'app_id', how = 'inner')
merged_data.to_csv('merged_data.csv', index = False)