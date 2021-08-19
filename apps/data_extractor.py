import streamlit as st
from apps import model_perspective as mp
import pandas as pd
from data import *

def data_pie_chart():
    
  values = mp.quiz();

  key = ['Procedural Fairness','Distributive Fairness']

  parents = ['Representativeness','Representativeness']
  
  return values, key, parents

def interpersonal_fairness():
  data = [{'Disrespect': 1, 'Invasion of Privacy':0,'Exposure to personal dangers':0, 'Inconsiderate Actions':1, 'Unwarranted Disclosure':0}, 
          {'Disrespect': 0, 'Invasion of Privacy':1,'Exposure to personal dangers':0.5, 'Inconsiderate Actions':0, 'Unwarranted Disclosure':1}, 
          {'Disrespect': 1, 'Invasion of Privacy':0.3,'Exposure to personal dangers':0.5, 'Inconsiderate Actions':1, 'Unwarranted Disclosure':0.5}
         ]
  df = pd.DataFrame(data, index = ['Loan Risk Assessment','Customer Dialog', 'Payment Investigations and repair'])

  return df

'''
Data for displaying the pipeline information 
'''
def pipeline_information():

    df = pd.read_csv('data/pipeline_information.csv')

    return df

