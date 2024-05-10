import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder
from processor import encode,split_matchup,rolling_average,combine,clean_df,team_list

def get_averages(team):
    df = pd.DataFrame()
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable = team_list.get(team))  
    games = gamefinder.get_data_frames()[0].head()
    games['HOME'] = 0
    games['AWAY'] = 0
    games['OPPONENT'] = ""
    split_matchup(games)
    games_1 = clean_df(df=games)
    games_2 = encode(df = games_1)
    rolling_avg = rolling_average(df=games_2)
    return rolling_avg

def get_averages_combined(teamx,teamy):
    rolling_x= get_averages(teamx)
    rolling_y =get_averages(teamy)
    rolling_final = combine(rolling_x,rolling_y)
    return rolling_final
    