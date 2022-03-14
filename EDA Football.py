import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re

st.title('NFL Football (Rushing) Stats Explorer')

st.markdown("""
This app performs simple webscraping of NFL Football player rushing stats data!
Come back soon to be able to see other stats (passing, receiving, etc.)!
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/).
""")

# Sidebar - stat selection
#unique_stat = ['passing',  'rushing',  'receiving',  'scrimmage',  'stats',  'defense',  'kicking',  'returns',  'scoring',
#'passing_advanced',  'Rushing_advanced',  'Receiving_advanced',  'Defense_advanced',  'advanced',
#'fantasy',  'redzone-passing',  'redzone-rushing',  'redzone-receiving']
#selected_stat = st.sidebar.selectbox('Stat', unique_stat)


st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1990,2022))))

# Web scraping of NFL player stats
# https://www.pro-football-reference.com/years/2019/rushing.htm
#@st.cache
def passing_data(year):
    url = "https://www.pro-football-reference.com/years/" + str(year) + "/passing.htm"
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    #raw['Wins'] = re.split(r'[\s-]+', raw.QBrec)
    #raw[['Wins','Losses','Ties']] = raw.QBrec.str.split('-', expand=True)
    #raw.Wins= raw.Wins.astype(str).astype(int)
    #raw.Losses= raw.Losses.astype(str).astype(int)
    #raw.Ties= raw.Ties.astype(str).astype(int)
    #raw.WinPct = raw.Wins / (raw.Wins + raw.Losses + raw.Ties)
    playerstats = raw.drop(['Rk','QBrec'], axis=1)
    return playerstats
playerstats = passing_data(selected_year)

# change data types
#playerstats['QBrec'] = playerstats['QBrec'].astype(str).astype(float)
playerstats['Y/C'] = playerstats['Y/C'].astype(str).astype(float)
playerstats['QBR'] = playerstats['QBR'].astype(str).astype(float)
playerstats['4QC'] = playerstats['4QC'].astype(str).astype(float)
playerstats['GWD'] = playerstats['GWD'].astype(str).astype(float)

def rushing_data(year):
    url = "https://www.pro-football-reference.com/years/" + str(year) + "/rushing.htm"
    html = pd.read_html(url, header = 1)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = rushing_data(selected_year)

def receiving_data(year):
    url = "https://www.pro-football-reference.com/years/" + str(year) + "/receiving.htm"
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = receiving_data(selected_year)

def scrimmage_data(year):
    url = "https://www.pro-football-reference.com/years/" + str(year) + "/scrimmage.htm"
    html = pd.read_html(url, header = 1)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk','Att', 'Y/R', 'Y/Tgt', 'Yds.1', 'TD.1','Lng.1','Y/A','Y/G.1','A/G'], axis=1)
    return playerstats
playerstats = scrimmage_data(selected_year)

def defense_data(year):
    url = "https://www.pro-football-reference.com/years/" + str(year) + "/defense.htm"
    html = pd.read_html(url, header = 1)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk','FF','Fmb','FR','Yds.1','TD.1','Comb','Solo','Ast','TFL','QBHits'], axis=1)
    return playerstats
playerstats = defense_data(selected_year)

def rushing_data(year):
    url = "https://www.pro-football-reference.com/years/" + str(year) + "/rushing.htm"
    html = pd.read_html(url, header = 1)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = rushing_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['RB','QB','WR','FB','TE']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

# Download player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot()
