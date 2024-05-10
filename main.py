import streamlit as st
import os
import pickle
import cv2 as cv
from extractor import get_averages_combined
st.set_page_config(layout='wide')

teams = ['ATL','BOS','CLE','NOP','CHI', 'DAL','DEN', 'GSW','HOU', 'LAC','LAL','MIA','MIL',
        'MIN','BKN','NYK','ORL','IND','PHI','PHX','POR','SAC','SAS','OKC','TOR','UTA','MEM','WAS','DET','CHA']

@st.cache_data
def store_logo_path(path):
    logo_files =  os.listdir(path)
    return logo_files

@st.cache_resource
def load_model():
    with open('Artificats\model.pkl', 'rb') as file:  
        model = pickle.load(file)
    return model

@st.cache_data
def resize(path):
    img = cv.imread(path)
    dimensions = (250,250)
    img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    return cv.resize(img,dimensions,interpolation=cv.INTER_AREA)

def show_image(team_name,images_path):
    for image_file in images_path:
        splits = image_file.split('.')
        if team_name == splits[0]:
            path = os.path.join('logos',image_file)
            resized_image = resize(path)
            st.image(resized_image, use_column_width="auto",output_format="auto")

def main():
    model = load_model()
    logo_path = store_logo_path("logos")
    st.markdown(
        """
        <style>
            .centered-header {
                text-align: center;
            }
        </style>
        
        <h1 class="centered-header">NBA Win Predictor</h1>
        """,
        unsafe_allow_html=True
    )
    col1,col2,col3,col4 = st.columns([1,1,1,2], gap="large")
    with col1:
        home_team = st.selectbox("",options = teams, index=None, placeholder = "Select Home team")
        st.header("Home Team")
        show_image(team_name= home_team,images_path=logo_path)
    with col2:
        for i in range(7):
            st.write("                                         ")
        st.markdown(
        """
        <style>
            .centered-header {
                text-align: center;
            }
        </style>
        
        <h1 class="centered-header">VS</h1>
        """,
        unsafe_allow_html=True
    )
        submit = st.button("Fight",use_container_width=True)
    with col3:
        away_team = st.selectbox("",options = teams, index=None, placeholder = "Away Home team")
        st.header("Away Team")
        show_image(team_name= away_team,images_path=logo_path)
    with col4:
        if submit:
            if home_team != None and away_team!= None:
                data = get_averages_combined(home_team,away_team)
                result = model.predict(data)
                st.header("Winning Team")
                if result[0] == home_team:
                    show_image(team_name= home_team,images_path=logo_path)
                else:
                    show_image(team_name= away_team,images_path=logo_path)
                st.balloons()
            
        


if __name__ == "__main__":
    main()