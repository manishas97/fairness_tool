import streamlit as st
from sklearn import tree
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode
from apps import data_extractor
import pandas as pd
import numpy as np
import csv
import time

#Global variables :

main_df_global = pd.read_csv('/content/drive/MyDrive/fairness_tool/data/data_tech.csv')
main_key = ["Components", "Sub-components", "Sub-sub component"]


@st.cache(allow_output_mutation=True)
def save_ticker(ticker):
  return ticker

def enter_stages(df):
    return df 

def select_stages():
  tickers = {}
  st.header("Please select the stages relevant to your model")
  stages_pipeline = ["Data Pre-processing", "Feature Engineering", "Evaluation"]

  for i in range(len(stages_pipeline)):
    tickers[stages_pipeline[i]] = st.checkbox(stages_pipeline[i])
  
  ticker = {k: v for k, v in tickers.items() if v==True}
  
  st.write(ticker)

  return ticker

def set_stages(saved_stages):

  df = pd.DataFrame(columns=saved_stages)
  new_df = enter_stages(df)

  return new_df

def selection_mode():
  
  selection_mode = st.sidebar.radio("Selection Mode", ['single','multiple'])
  
  return selection_mode

def checkbox():

  gsc = st.sidebar.checkbox("Group checkbox select children", value=True)
  
  gsf = st.sidebar.checkbox("Group checkbox includes filtered", value=True)

  return gsf , gsc

def grid_generator(selection_mode, df, gsc, gsf, ump, update_mode):
  
  gb = GridOptionsBuilder.from_dataframe(df)
  gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=True)

  gb.configure_selection(selection_mode,use_checkbox=True, groupSelectsChildren= gsc,
                         groupSelectsFiltered=gsf)

  gb.configure_grid_options(domLayout='normal')
  gb.configure_grid_options(enableRowSelection=True)
  my_list_of_options = ['Option 1', 'Option 2', 'Option 3']
  gb.configure_column("Components", editable=True, cellEditor='agSelectCellEditor',
                      cellEditorParams={'values': my_list_of_options})
  filters = gb.build()
  grid_response = AgGrid(
      df, gridOptions=filters,
      width='100%', 
      update_mode=ump, 
      editable=True,allow_unsafe_jscode=True,
      cellEditor='agSelectCellEditor',
      cellEditorParams={'values': my_list_of_options}
      )

  return grid_response

def get_data_tech(main_df, k):
  
  df = main_df[[k]]

  st = df[k].unique()

  new_df = pd.DataFrame(st, columns=[k])

  return new_df

def tick_boxes():
  ticker = select_stages();

  saved_stages = save_ticker(ticker);

  #df = set_stages(saved_stages);

  set_stages_1 = st.button("Set Stages")

#Create a df where parents are set as index
def create_df_parent(parent_df, key):
  parent_index_df = parent_df.set_index(key)
  return parent_index_df

def select_child_component(key, parent_comp): 
  child_comp = [cc[key] for cc in parent_comp]  
  return child_comp

@st.cache(allow_output_mutation=True)
def selected_components():
    return []

def display_grids(key, parent_df, parent_comp):

  #Create a dataframe to set parents as index 
  parent_index_df = create_df_parent(parent_df, key)
  
  #Find the selected parent components in the df, to display their children
  child_comp = select_child_component(key, parent_comp)
  
  #Create new dataframe out of these children 
  display_df = parent_index_df[parent_index_df.index.isin(child_comp)]

  #return the new dataframe 
  return display_df

def get_parent_comp(grid_response):

  #Get the grid response
  parent_comp = grid_response['selected_rows']

  return parent_comp


@st.cache
def get_data(main_key):
    data = {main_key[0]:['Click to fill'], main_key[1]: ['Click to fill'], main_key[2]:['Click to fill']}
    return data

def get_main_df(x):
  main_df = x;
  return main_df

def get_responses():
    responses = []
    return responses


def unnesting(df, explode, axis):

  if axis == 1:
    df1 = pd.concat([df[x].explode() for x in explode], axis=1)
    return df1.join(df.drop(explode, 1), how='left')
  else:
    df1 = pd.concat([
      pd.DataFrame(df[x].tolist(), index=df.index).add_prefix(x) for x in explode], axis=1)
    return df1.join(df.drop(explode, 1), how='left')


def variable_settings():

  response = get_responses();

  main_df = main_df_global

  #Get the main data, and parent data

  #Allow ticking process to work
  update_mode = 'SELECTION_CHANGED'
  ump = GridUpdateMode.__members__[update_mode]

  #Allow checkbox functionality
  gsf, gsc = checkbox();

  #Define the parent dataframe
  parent_df = main_df;

  display_df = main_df;
  i = 0;

  #Define the new key
  key = ["Components", "Sub-components", "Sub-sub component"]

  return response, main_df, update_mode, ump, gsc, gsf, parent_df, display_df, i, key

st.spinner();
def run_grids(response, main_df, update_mode, ump, gsc, gsf, parent_df, display_df, i, key):

    columns = st.beta_columns(3)
    selection_mode = 'multiple'

    for k in key:

      if (k == "Sub-sub component"):

          selection_mode = 'multiple'
      else:
          selection_mode = 'multiple'

      display_df = get_data_tech(display_df, k);

      with columns[i]:
          grid_response = grid_generator(selection_mode, display_df, gsc, gsf, ump, update_mode)

          fin_list = grid_response['selected_rows']

          fin_comp = [i[k] for i in fin_list if k in i]

          response.append(fin_comp)
          i = i + 1

      if (k == "Sub-sub component"):
          break;

      parent_comp = get_parent_comp(grid_response);

      display_df = display_grids(k, parent_df, parent_comp)

      key = key[1:]


    #main_df = get_new_entry(main_df_global);

    save_ss_comp = st.button('Add sub-sub component')
    response_final = selected_components()

    if save_ss_comp:
      response_final.append(response)

    f_p = selected_components();

    new_df = pd.DataFrame(response_final, columns=["Components", "SComponents", "SSComponents"])
    y = unnesting(new_df, ["SComponents", "SSComponents"], axis=1)

    pipeline_grid = grid_generator(selection_mode, y, ump, gsc, gsf, update_mode)

    return pipeline_grid


def app():

  response, main_df, update_mode, ump, gsc, gsf, parent_df, display_df, i, key = variable_settings();
  run_grids(response, main_df, update_mode, ump, gsc, gsf, parent_df, display_df, i, key)


def get_new_entry(main_df_global):
  c1 = st.beta_container()

  with c1:
    st.write('Add your own component')
    df = get_data(main_key)
    grid_return = AgGrid(main_df_global, editable=True)

    save_entry = st.button('Save in system')

    if save_entry:
        #df_entry = grid_return['data']

        with open('data/data_tech.csv', 'a') as f:
          main_df_global.to_csv(f, header=False)

        return main_df_global

    return main_df_global










    

 





  

  
  

  

      


  

  
  

  

  








  

 
