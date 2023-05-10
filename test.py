import streamlit as st
from chembl_webresource_client.new_client import new_client
import pandas as pd

# Create a text input box for the user to enter search query
search_query = st.text_input("Enter search query")

# Search for the target using the search query
target = new_client.target
target_query = target.search(search_query)
targets = pd.DataFrame.from_dict(target_query)

# Check if targets DataFrame is not empty
if not targets.empty:
    # Create a list of target IDs from the DataFrame
    target_ids = targets['target_chembl_id'].tolist()

    # Select a target ID from the list using a dropdown menu
    selected_target_id = st.selectbox("Select target ID", options=target_ids)

    # Get the target record for the selected target ID
    target_record = target.get(selected_target_id)

    # Get a particular column value from the target record
    column_name = 'organism'
    column_value = target_record[column_name]

    # Display the column value to the user
    st.write(f"{column_name}: {column_value}")
else:
    st.write("No targets found for the given search query.")
