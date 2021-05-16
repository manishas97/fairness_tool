import streamlit as st
import pandas as pd
import numpy as np
from apps import model_perspective, data_extractor 
from pandasql import sqldf

import pydbgen 
from pydbgen import pydbgen as pg

def app():
    st.title('Home')
    st.write('This will contain a guide to using the tool and some contact information and such')
    
    df = data_extractor.interpersonal_fairness()
    st.write(df)
    x = sqldf("SELECT * FROM df WHERE DISRESPECT = 0")
    st.write(x)
    

