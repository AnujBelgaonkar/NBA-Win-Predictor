from sklearn.preprocessing import LabelEncoder
import pandas as pd

team_list = {'ATL': 1610612737,
 'BOS': 1610612738,
 'CLE': 1610612739,
 'NOP': 1610612740,
 'CHI': 1610612741,
 'DAL': 1610612742,
 'DEN': 1610612743,
 'GSW': 1610612744,
 'HOU': 1610612745,
 'LAC': 1610612746,
 'LAL': 1610612747,
 'MIA': 1610612748,
 'MIL': 1610612749,
 'MIN': 1610612750,
 'BKN': 1610612751,
 'NYK': 1610612752,
 'ORL': 1610612753,
 'IND': 1610612754,
 'PHI': 1610612755,
 'PHX': 1610612756,
 'POR': 1610612757,
 'SAC': 1610612758,
 'SAS': 1610612759,
 'OKC': 1610612760,
 'TOR': 1610612761,
 'UTA': 1610612762,
 'MEM': 1610612763,
 'WAS': 1610612764,
 'DET': 1610612765,
 'CHA': 1610612766}

req_cols = ['TEAM_ID_5_x',
 'WL_5_x',
 'FT_PCT_5_x',
 'DREB_5_x',
 'REB_5_x',
 'AST_5_x',
 'BLK_5_x',
 'TOV_5_x',
 'PF_5_x',
 'PLUS_MINUS_5_x',
 'HOME_5_x',
 'TEAM_ID_5_y',
 'WL_5_y',
 'PTS_5_y',
 'OREB_5_y',
 'DREB_5_y',
 'BLK_5_y',
 'TOV_5_y',
 'PLUS_MINUS_5_y',
 'AWAY_5_y']

def encode(df):
    le = LabelEncoder()
    df['WL'] = le.fit_transform(df['WL']) 
    return df

def split_matchup(df):
    for index,matchup in df.iterrows():
        temp = matchup.MATCHUP.split()
        if temp[1] == 'vs.':
            df.HOME[index] = 1
            df.AWAY[index] = 0
            df.OPPONENT[index] = team_list.get(temp[2])
        elif temp[1] == '@':
            df.AWAY[index] = 1
            df.HOME[index] = 0
            df.OPPONENT[index] =  team_list.get(temp[2])
    del df['MATCHUP']

def rolling_average(df):
    rolling_cols = [f"{col}_5" for col in df.columns]
    df.columns = rolling_cols
    df = df.rolling(5).mean()
    rolling_df = df.dropna()
    return rolling_df

def combine(df_x,df_y):
    combined_df = pd.merge(df_x, df_y, left_index=True, right_index=True, suffixes=('_x', '_y'))
    combined_df = combined_df[req_cols]
    return combined_df

def clean_df(df):
    try:
        del df['TEAM_ABBREVIATION']
        del df['TEAM_NAME']
        del df['GAME_DATE']
        del df['SEASON_ID']
        del df['GAME_ID']
        return df
    except:
        print("Error")