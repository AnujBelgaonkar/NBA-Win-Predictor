import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder
from src.Functionality.processor import encode,split_matchup,rolling_average,combine,clean_df,team_list
import warnings

warnings.filterwarnings("ignore")

def get_data(team):
    df = pd.DataFrame()
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable = team_list.get(team))  
    games = gamefinder.get_data_frames()[0].head()
    games['HOME'] = 0
    games['AWAY'] = 0
    games['OPPONENT'] = ""
    split_matchup(games)
    games_1 = clean_df(df=games)
    games_2 = encode(df = games_1)
    return games_2

def data_avg(df):
    df_avg = df.rolling(5).mean()
    df_avg = df_avg.dropna()
    result = pd.concat([df, df_avg]).reset_index(drop=True)
    del result['TEAM_ID_5_x']
    del result['TEAM_ID_5_y']
    return result


def get_averages(team):
    df = get_data(team)
    rolling_avg = rolling_average(df)
    return rolling_avg,df

def get_averages_combined(teamx,teamy):
    rolling_x,data_x= get_averages(teamx)
    rolling_y,data_y =get_averages(teamy)
    rolling_final = combine(rolling_x,rolling_y)
    data = combine(data_x,data_y)
    data = pd.merge(data_x, data_y, left_index=True, right_index=True, suffixes=('_x', '_y'))
    del data['HOME_5_y']
    del data['AWAY_5_y']
    del data['OPPONENT_5_y']
    del data['OPPONENT_5_x']
    del data['HOME_5_x']
    del data['AWAY_5_x']
    del data['MIN_5_y']
    del data['MIN_5_x']
    past_results = data_avg(data)
    return rolling_final,past_results
    