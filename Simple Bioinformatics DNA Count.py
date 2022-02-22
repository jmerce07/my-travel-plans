######################
# Import libraries
######################

import pandas as pd
import streamlit as st
import altair as alt #for the graph
from PIL import Image #to display the image

######################
# Page Title
######################

# display the image
image = Image.open('Stockphoto-DNA-Simple2.png')

st.image(image, use_column_width=True) #allow image to expand to the column width

#Header 
st.write("""
# DNA Nucleotide Count Application
This app counts the nucleotide composition of query DNA!
***
""")
# The "***" above displays a horizontal line on the page 

######################
# Input Text Box
######################

#st.sidebar.header('Enter DNA sequence')
st.header('Enter DNA sequence')

# need a double-whitespace before \n to get a newline in st.write for streamlit1.1.0
sequence_input = ">DNA Query \nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG  \nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC  \nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

#sequence = st.sidebar.text_area("Sequence input", sequence_input, height=250)
sequence = st.text_area("Sequence input", sequence_input.upper(), height=250)
sequence = sequence.splitlines()
sequence = sequence[1:] # Skips the sequence name (first line)
sequence = ''.join(sequence) # Concatenates list to string
sequence = sequence.upper() #upper case all characters

st.write("""
***
""")

## Prints the input DNA sequence
st.header('INPUT (DNA Query)')
st.write(sequence)

## DNA nucleotide count
st.header('OUTPUT (DNA Nucleotide Count)')

### 1. Print dictionary
st.subheader('1. Count via dictionary')
def DNA_nucleotide_count(seq):
  d = dict([
            ('A',seq.count('A')),
            ('T',seq.count('T')),
            ('G',seq.count('G')),
            ('C',seq.count('C'))
            ])
  return d

X = DNA_nucleotide_count(sequence)

#X_label = list(X)
#X_values = list(X.values())

# Show the dictionary
X

### 2. Print text
st.subheader('2. Count via text')
st.write('There are  ' + str(X['A']) + ' adenine (A)')
st.write('There are  ' + str(X['T']) + ' thymine (T)')
st.write('There are  ' + str(X['G']) + ' guanine (G)')
st.write('There are  ' + str(X['C']) + ' cytosine (C)')

### 3. Display DataFrame
st.subheader('3. Display Table')
df = pd.DataFrame.from_dict(X, orient='index')
df = df.rename({0: 'count'}, axis='columns')
df.reset_index(inplace=True)
df = df.rename(columns = {'index':'nucleotide'})
st.write(df)

### 4. Display Bar Chart using Altair
st.subheader('4. Distribution of Nucleotides in the Sequence')
p = alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
).configure_axis(
    labelFontSize=20,
    titleFontSize=20
)
p = p.properties(
    width=alt.Step(80)  # controls width of bar.
)
st.write(p)