import streamlit as st
import os
import pickle
import cv2 as cv
from src.Functionality.extractor import get_averages_combined   
from src.Functionality.background import apply_background

# Set page configuration
st.set_page_config(
    page_title="NBA Win Predictor",
    layout='wide', 
    page_icon=":basketball:",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "I love basketball and I'm an avid NBA fan. This is my passion project."
    }
)

st.session_state.update(st.session_state)
# List of NBA teams
teams = ['ATL', 'BOS', 'CLE', 'NOP', 'CHI', 'DAL', 'DEN', 'GSW', 'HOU', 'LAC', 'LAL', 'MIA', 'MIL',
         'MIN', 'BKN', 'NYK', 'ORL', 'IND', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'OKC', 'TOR', 'UTA', 'MEM', 'WAS', 'DET', 'CHA']

# Function to store logo file paths
@st.cache_data
def store_logo_path(path):
    logo_files = os.listdir(path)
    return logo_files

# Function to load the trained model
@st.cache_resource
def load_model():
    with open('Artificats/model.pkl', 'rb') as file:  
        model = pickle.load(file)
    return model

# Function to resize the logo images
@st.cache_data
def resize(path):
    img = cv.imread(path)
    dimensions = (300, 250)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    return cv.resize(img, dimensions, interpolation=cv.INTER_AREA)

# Function to display team logos
def show_image(team_name, images_path):
    for image_file in images_path:
        splits = image_file.split('.')
        if team_name == splits[0]:
            path = os.path.join('logos', image_file)
            resized_image = resize(path)
            st.image(resized_image, use_column_width="auto", output_format="auto")

# Function to persist selected team
def select_persist(HorA):
    if st.session_state[HorA] is None:
        return None
    elif HorA == 'Home':
        return teams.index(st.session_state['Home'])
    else:
        return teams.index(st.session_state['Away'])

def main():
    # Load the trained model
    model = load_model()
    apply_background()
    logo_path = store_logo_path("logos")
    
    # Set session states
    if 'Home' not in st.session_state:
        st.session_state.Home = None
    if 'Away' not in st.session_state:
        st.session_state.Away = None

    # Title
    st.markdown("<h1 style='text-align: center;'>NBA Win Predictor</h1>", unsafe_allow_html=True)
    
    # Side-by-side layout
    column1,column2 = st.columns([2,1], gap = "large")
    
    with st.container():
        # Home team selection
        with column1:
            col1, col2, col3 = st.columns([1, 1, 1], gap="small")
            with col1:
                st.header("Home Team")
                home_team = st.selectbox("first select box", options=teams, index=select_persist('Home'), placeholder="Select Home team", key="Home",label_visibility='collapsed')
                show_image(team_name=home_team, images_path=logo_path)
            
            # "VS" text
            with col2:
                for _ in range(17):
                    st.write(" ")
                st.markdown("<h1 style='text-align: center;'>VS</h1>", unsafe_allow_html=True)
                submit = st.button("PLAY", use_container_width=True)
            # Away team selection
            with col3:
                st.header("Away Team")
                away_team = st.selectbox("second select box", options=teams, index=select_persist('Away'), placeholder="Select Away team", key="Away",label_visibility='collapsed')  
                show_image(team_name=away_team, images_path=logo_path)

        # Display winning team
        with column2:
            result_displayed = False
            if submit:
                if home_team is not None and away_team is not None:
                    data, performances = get_averages_combined(home_team, away_team)
                    result = model.predict(data)
                    st.markdown("<h1 style='text-align: center;'>Winning Team</h1>", unsafe_allow_html=True)
                    for _ in range(4):
                        st.write(" ")
                    if result[0] == 0:
                        show_image(team_name=home_team, images_path=logo_path)
                    else:
                        show_image(team_name=away_team, images_path=logo_path)
                    result_displayed = True
                    st.balloons()
    
    # Display last 5 games comparison
    with st.container():
        if result_displayed:
            st.session_state['df'] = performances
            st.markdown("---")
            st.markdown("### Last 5 Games Comparison")
            st.page_link("pages/Last 5 Games Comparision.py", label = "Go")


if __name__ == "__main__":
    main()