import streamlit as st

st.title('Generative Chemistry')
user_target = st.text_input("Target", value="Enter Your Target Protein", max_chars=50)
target_index = st.number_input("Target Index",step=1,help='Enter the index number of the target you would want to proceeed with')

options = ['IC50', 'Molecular Weight', 'logP']
selected_options = st.multiselect('Select options', options)
if 'Molecular Weight' in selected_options:
    slider_value = st.slider('Select a value', 0, 15000, 100)

smiles = st.file_uploader("Upload your simles file", type=['smi'])

submit = st.button("Generate")
if submit:
    st.write("You submitted your requirements! Please wait while we generate your request")




