from rdkit import Chem
from rdkit.Chem import PandasTools
from rdkit import DataStructs
from rdkit.Chem import Draw
from rdkit.Chem.Draw import IPythonConsole
import pandas as pd
from chembl_webresource_client.new_client import new_client
import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

target_name = st.text_input("Enter a target name")

if target_name:
    target = new_client.target
    target_query = target.search(target_name)
    targets = pd.DataFrame.from_dict(target_query)

    targets.drop(['species_group_flag', 'cross_references', 'target_components', 'tax_id'], axis=1, inplace=True)
    targets.reset_index(inplace=True, drop=False)
    targets.rename(columns={'index': 'index_number'}, inplace=True)

    #df1 = pd.read_csv('targets.csv')
    gd = GridOptionsBuilder.from_dataframe(targets)
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridoptions = gd.build()

    grid_table = AgGrid(targets, height=500,width=10000, gridOptions=gridoptions,update_mode=GridUpdateMode.SELECTION_CHANGED,theme='dark')


    st.write('## Selected')
    selected_row = grid_table["selected_rows"]
    if len(selected_row) > 0:
      st.dataframe(selected_row)

      selected_names = selected_row[0]
      selected_target = selected_names.get("target_chembl_id")
      #st.write(selected_target)

      activity = new_client.activity
      res = activity.filter(target_chembl_id=selected_target).filter(standard_type="IC50")

      df1=pd.DataFrame.from_dict(res)
      #df1

      df1 = df1.reset_index(drop=True)
      df2 = df1[df1['standard_value'].notna()]

      


      bioactivity_class = []
      for i in df2.standard_value:
        if float(i) >= 10000:
          bioactivity_class.append("inactive")
        elif float(i) <=1000:
          bioactivity_class.append("active")
        else:
          bioactivity_class.append("intermediate")

      selection = ['molecule_chembl_id', 'canonical_smiles', 'standard_value']
      df3 = df2[selection]

      df4=pd.concat([df3, pd.Series(bioactivity_class)], axis=1)
      df4

      list = df3["canonical_smiles"].tolist()
      #list

      mol_list = [Chem.MolFromSmiles(smiles) for smiles in list]

      # generate 2D depictions of molecules
      img_list = [Draw.MolToImage(mol) for mol in mol_list]

      # display images in a grid using Streamlit
      st.image(img_list, width=200, caption=list)
    else:
      st.write("No row selected")     

else:
    st.write("Enter a target name to search")


