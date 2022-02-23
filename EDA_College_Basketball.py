import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('College Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of College Basketball player stats data!
* **Python libraries:** base64, pandas, streamlit, numpy
* **Data source:** [sports-reference.com](https://www.sports-reference.com/cbb/).
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1949,2023))))
#team = "north-carolina"

# Web scraping of College player stats
@st.cache
def load_data(year):
    url = "https://www.sports-reference.com/cbb/schools/north-carolina/" + str(year) + ".html"
    html = pd.read_html(url, header = 0)
    df = html[5]
    raw = df.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selected_year)
#st.dataframe(playerstats)

# Sidebar - Team selection
#sorted_unique_team = sorted(playerstats.Tm.unique())
#selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Player selection
sorted_unique_Player = sorted(playerstats.Player.unique())
selected_Player = st.sidebar.multiselect('Player', sorted_unique_Player, sorted_unique_Player)

# Sidebar - Position selection
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
#df_selected_Player = playerstats[(playerstats.Player.isin(selected_Player)) & (playerstats.Pos.isin(selected_pos))]
df_selected_Player = playerstats[(playerstats.Player.isin(selected_Player))]
df_selected_Player['FG%'] = df_selected_Player['FG%'].astype(str).astype(float)
df_selected_Player['3P%'] = df_selected_Player['3P%'].astype(str).astype(float)
df_selected_Player['2P%'] = df_selected_Player['2P%'].astype(str).astype(float)
df_selected_Player['eFG%'] = (df_selected_Player['FG'] + 0.5 * df_selected_Player['3P']) / df_selected_Player['FGA']
df_selected_Player['FT%'] = df_selected_Player['FT%'].astype(str).astype(float)

st.header('Display Player Stats of Selected Player(s)')
st.write('Data Dimension: ' + str(df_selected_Player.shape[0]) + ' rows and ' + str(df_selected_Player.shape[1]) + ' columns.')
st.dataframe(df_selected_Player)

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_Player), unsafe_allow_html=True)

# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_Player.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')
    st.set_option('deprecation.showPyplotGlobalUse', False) #hides warning
    
    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)

    st.pyplot()