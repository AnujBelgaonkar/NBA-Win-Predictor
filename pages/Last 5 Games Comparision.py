import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#st.session_state.update(st.session_state)
if 'Home' not in st.session_state:
        st.session_state.Home = None
if 'Away' not in st.session_state:
        st.session_state.Away = None
st.session_state['Away'] = st.session_state['Away']
st.session_state['Home'] = st.session_state['Home']
if 'df' not in st.session_state:
    st.write("Select Home and Away teams and Click the Fight button for their stats")
else:
    performances = st.session_state['df']

    st.page_link("app.py", label="Go Back")
    st.write("Note : When hovering over data points '_x' indicate Home team and '_y' indicate Away team.")
    column_pairs = [(col[:-2], col[:-2]+'_y') for col in performances.columns if col.endswith('_x')]
    x = ['1', '2', '3', '4', '5', 'Average']

    num_rows = len(column_pairs) // 2 + len(column_pairs) % 2
    fig = make_subplots(rows=num_rows, cols=2, subplot_titles=[x_col.replace('_5', ' Home') + '  vs  ' + y_col.replace('_5_y', ' Away') for x_col, y_col in column_pairs])

    for i, (x_col, y_col) in enumerate(column_pairs):
        row = i // 2 + 1
        col = i % 2 + 1
        
        fig.add_trace(go.Scatter(name=x_col+'_x', x=x, y=performances[x_col+'_x'], mode='lines+markers', showlegend=False), row=row, col=col)
        fig.add_trace(go.Scatter(name=y_col, x=x, y=performances[y_col], mode='lines+markers', showlegend=False), row=row, col=col)

    fig.update_layout(height=2450, width=1400)

    for i, (x_col, y_col) in enumerate(column_pairs):
        fig.update_xaxes(title_text='Match', row=i//2+1, col=i%2+1)
        fig.update_yaxes(title_text='Value', row=i//2+1, col=i%2+1)

    st.plotly_chart(fig)
