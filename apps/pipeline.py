import streamlit as st
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import tree
from sklearn.datasets import load_wine
from IPython.display import SVG
from graphviz import Source
from IPython.display import display                               
import pandas as pd
import igraph
from igraph import Graph, EdgeSeq

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots



df = pd.read_csv('/content/drive/MyDrive/streamlit-multiapps-master/data/data_dimensions.csv')
df_tech = pd.read_csv('/content/drive/MyDrive/streamlit-multiapps-master/data/data_tech.csv')
df_def = pd.read_csv('/content/drive/MyDrive/streamlit-multiapps-master/data/data_def.csv')
'''
 = ['Dimension', 'Concept', 'Specification', 'Description'] # levels used for the hierarchical chart
color_columns = ['Dimension', 'Concept']
value_column = 'Specification'
'''
def app():
  
  with st.beta_container():
    st.write('Explore fairness definitions')
    fig = px.treemap(df_def,path=['Fairness Definition'], values=None)
    fig.update_layout(uniformtext=dict(minsize=9, mode='hide'))
    st.plotly_chart(fig, use_container_width=True)

  with st.beta_container():
    st.write('Explore fairness dimensions')
    fig = px.treemap(df,path=['Dimension', 'Concept', 'Specification'], values=None)
    fig.update_layout(uniformtext=dict(minsize=9, mode='hide'))
    st.plotly_chart(fig, use_container_width=True)

  with st.beta_container():
    st.write('Explore fairness within the model development pipeline')
    fig = px.treemap(df_tech,path=['Components', 'Sub-components', 'Sub-sub component'], values=None)
    fig.update_layout(uniformtext=dict(minsize=9, mode='hide'))
    st.plotly_chart(fig, use_container_width=True)




 


  
                

