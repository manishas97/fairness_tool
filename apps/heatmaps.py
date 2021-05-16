import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb 
import numpy as np


from apps import data_extractor as d_e
    

def app():
  st.title('Understand Social implications')

  df = d_e.interpersonal_fairness();
  
  st.write(df)

  fig, ax = plt.subplots()
  data = df
  ax = sb.heatmap(data, annot=True)
  st.pyplot(fig)






