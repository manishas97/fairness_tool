import streamlit as st
from sklearn import tree
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder
from apps import data_extractor
import pandas as pd


@st.cache(allow_output_mutation=True)
def save_ticker(ticker):
  return ticker

def enter_stages(df):
    return df 


def select_stages():
  tickers = {}
  st.header("Please select the stages relevant to your model")
  stages_pipeline = ["Data Pre-processing", "Feature Engineering", "Text-to-speech"]

  for i in range(len(stages_pipeline)):
    tickers[stages_pipeline[i]] = st.checkbox(stages_pipeline[i])
  
  ticker = {k: v for k, v in tickers.items() if v==True}
  
  st.write(ticker)

  return ticker

def set_stages(saved_stages):

  df = pd.DataFrame(columns=saved_stages)
  new_df = enter_stages(df)

  return new_df


def grid_generator(df):

  grid_return = AgGrid(df, key='grid_main', editable=True)
  
  return grid_return


def app():
  ticker = select_stages();
  saved_stages = save_ticker(ticker);
  df = set_stages(saved_stages);

  set_stages = st.button("Set Stages")

  if set_stages:
      grid_generator(df)
  

  

  








  

 
