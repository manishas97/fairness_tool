from google.cloud import firestore
import SessionState
import streamlit as st
import pandas as pd
from apps import create_your_pipeline, markdowns, firestore_calls as fc
from apps import toc
import random
import time
import collections
import os
import technical_data
import utils

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json('firestore-key.json')

relevance = ["Relevant", "Not relevant"]

#Selected Mode : Exploration
def exploration(selected_model):
    
  inequalities = st.expander(label='Indicate inequalities')
  bias = st.expander(label='Indicate bias')
  procedural = st.expander(label='Indicate Procedural Fairness')
  distributive = st.expander(label='Indicate Distributive Fairness')

  with inequalities:
    set_model_inequalities(selected_model)
  
  with bias:

    set_model_bias(selected_model)

  with procedural:
    set_model_procedural(selected_model)

  with distributive:

    set_model_distributive(selected_model)


def set_model_inequalities(selected_model):
  
  #Explore inequalities

  inequalities = fc.get_notions(social_fairness_notion="Fairness Inequalities")
    
  fc.pagination(inequalities, "b5", "b6")

  social_fairness_notion = "Fairness Inequalities"
  scale = relevance
  fc.set_model_requirements(selected_model, social_fairness_notion, scale)

def set_model_bias(selected_model):
    
  social_fairness_notion = "Bias"
  scale = relevance
  fc.set_model_requirements(selected_model, social_fairness_notion, scale)

def set_model_procedural(selected_model):
    
  social_fairness_notion = "Procedural Fairness"
  scale = relevance
  fc.set_model_requirements(selected_model, social_fairness_notion, scale)

def set_model_distributive(selected_model):
    
  social_fairness_notion = "Distributive Fairness"
  scale = relevance
  fc.set_model_requirements(selected_model, social_fairness_notion, scale)

def set_model_definitions(selected_model):

  social_fairness_notion = "Fairness Definitions"
  scale = relevance
  fc.set_model_requirements(selected_model, social_fairness_notion, scale)


def recommendation(selected_model):
    
  philosophies = st.expander(label='Fairness Philosophies')


  with philosophies:
  
    recommended_philosophies = fc.get_model_philosophies(selected_model)

    fc.pagination(recommended_philosophies, "b1", "b2")


def explore_definitions(selected_model):
  
  definitions = st.expander(label='Fairness Definitions')

  with definitions:
    
    #Display Recommended Definitions
    recommended_definitions = fc.get_model_definitions(selected_model)

    fc.pagination(recommended_definitions, "b3", "b4")

    #Display all definitions

    all_definitions = fc.get_notions(social_fairness_notion="Fairness Definitions")

    fc.pagination(all_definitions, "b11", "b12", "Explore All")

    st.write("")
    #Select your definition
    set_model_definitions(selected_model)


  
    
    
    
  


















'''
def indicate_fairness_dimensions(selected_model):

  guide = st.expander(label='Guide')
  dimensions = st.expander(label='Indicate Fairness Dimensions')
  with guide:

    markdowns.fairness_dimensions();

  with dimensions:
    moscow = ["Must", "Should", "Could"]
    fairness_types = ["Procedural", "Distributive"]
    doc_sel_mode = db.collection("Models").document(selected_model).collection("Fairness Requirements")

    i = 0

    values = []

    for doc in doc_sel_mode.stream():
        fairness_dim = doc.to_dict();

    for f in fairness_types:
        values = []
        doc_fairness = db.collection("Fairness Dimension").document(f)
        dict_fair = doc_fairness.get().to_dict()

        for k, v in dict_fair.items():
            for vk in v.keys():
                values.append(vk)
  	
        st.write("Category:", f)
        doc_fairness = db.collection("Fairness Dimension").document(f)
       
        with st.form(key=f):
            answer = {}
            c = len(values)
            for i in range(c):
              k = values[i]
              val = st.selectbox(values[i], moscow)
              answer[k] = val          
            use_case = st.text_input("Indicate any real-life use cases or additional information")
            answer['Use Cases'] = use_case
            submitted = st.form_submit_button('Submit')
            if submitted:
              st.write(answer)
              doc_ref = db.collection("Models").document(selected_model).collection("Fairness Requirements").document(f)
              doc_ref.set(answer)
    
    st.write('You have successully set all the fairness dimensions!')
'''
