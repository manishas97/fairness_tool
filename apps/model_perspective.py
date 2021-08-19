import streamlit as st
import numpy as np
import pandas as pd

from apps import interactive_guide
from apps import data_extractor

import plotly.express as px
import plotly.graph_objects as go

from collections import ChainMap

"""
Indicate the importance of each fairness notion 
"""

def quiz():

  questions = []

  question_1 = st.slider('Indicate the importance of procedural fairness', 0.0,10.0,step=0.1)
  question_2 = st.slider('Indicate the importance of distributive', 0.0,10.0 ,step=0.1)
  
  questions.append(question_1)
  questions.append(question_2)
  
  return questions

"""
Visualize the slider information

fairness notions : topic of the slider
values : slider value 
parents : parent topic of the slider, chosen in multi-select

"""

def pie_chart(key, parents, values):

  data = dict(
    character=key,
    parent=parents,
    value=values)

  fig = px.sunburst(
    data,
    names='character',
    parents='parent',
    values='value',
    color = 'value',
    color_continuous_scale='darkmint'
  )

  st.plotly_chart(fig)

def viewpoint():

  st.title('Please select your viewpoint')

  viewpoints = ("User","Developer","Owner")
  viewpoint = st.selectbox('Select your viewpoint', options = viewpoints)

  return viewpoint

@st.cache(allow_output_mutation=True)
def recordview():
  return {}

#TODO Add hash function

"""
Save all the slider data to visalize

"""
@st.cache(allow_output_mutation=True)
def persistdata():
    return {}

@st.cache(allow_output_mutation=True)
def savedata():
    return []

'''
Run the app. Call all containers and functions here. 

Called by app.py

'''

def app():

  with st.container():
    
    df_view = recordview();
    
    viewpoint_curr = viewpoint();

    button = st.button('Set View')
    if button:
      if viewpoint_curr: 
          df_view['viewpoint'] = viewpoint_curr;

  with st.container():

   values, key, parents = data_extractor.data_pie_chart();

   button_set_values = st.button("Set Values");

   pie_chart(key,parents,values);
  

  with st.container():
    
    df_quiz = persistdata();
     
    if button_set_values:
      if key and values:
        if len(key)==len(values):
          for i in range(len(key)):
              df_quiz[key[i]] = values[i], parents[i]
        else : 
          st.write('Error: Dict does not have same length has number of sliders')    
    
    button_save = st.button("Save")
    button_reset = st.button("Reset stored information (Warning : all records will be deleted")

    if button_reset:
      savedata().clear()

    if button_save:
        df_new = dict(ChainMap(df_quiz, df_view))
        savedata().append(df_new.copy())
        
  st.write(savedata())


    

    


  
   

    

  
  
  






