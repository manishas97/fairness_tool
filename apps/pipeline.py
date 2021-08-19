import streamlit as st
import pandas as pd
import plotly.express as px
from google.cloud import firestore
import SessionState
from apps import home

#df = pd.read_csv('data/data_dimensions.csv')
#df_tech = pd.read_csv('data/data_tech.csv')
#df_def = pd.read_csv('data/data_def.csv')

'''
 = ['Dimension', 'Concept', 'Specification', 'Description'] # levels used for the hierarchical chart
color_columns = ['Dimension', 'Concept']
value_column = 'Specification'

def explore_guide():
  
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
'''

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json('/content/drive/MyDrive/fairness_tool/firestore-key.json')
session_state = SessionState.get(checkboxed=False)
session_state.checkboxed = False

def app():

  #Setting your pipeline stages
  stages = ['Preprocessing', 'InProcessing', 'Postprocessing']
  selected_box = st.select_slider('Select the stage you want to explore', options=stages)

  docs = db.collection(u'Components').where(u'Stage', u'==', selected_box).stream()

  select_pipeline_stages = {}
  set_pipeline_stages = {}

  for doc in docs:
      if selected_box in select_pipeline_stages:
        select_pipeline_stages[selected_box].append(doc.id)
      else:
        select_pipeline_stages[selected_box] = [doc.id]

  with st.form(key=selected_box):
    st.write('Please select the relevant pipeline stages for your model. This pipeline will be appended to the model technical information. If you wish to change the pipeline stages, simply change your selection and click the "Set stages" button again')
    for v in select_pipeline_stages[selected_box]:
      option = st.checkbox(v, key = v)
      if option:
        if selected_box in set_pipeline_stages:
          set_pipeline_stages[selected_box].append(v)
        else:
          set_pipeline_stages[selected_box] = [v]
     
    submit_button = st.form_submit_button(label = 'Set ' + selected_box + ' stages')
   
  if submit_button:
    doc_ref = db.collection('Models').document('TestModel2').collection('Technical Information').document('New Pipeline')
    doc_ref.set(set_pipeline_stages)


  #Exploring as you go
    try:
      for doc in set_pipeline_stages[selected_box]:
          sub_collection = db.collection('Components').document(doc).collections()
          for sc in sub_collection:
            for sub_doc in sc.stream():
              sub_expander = st.beta_expander(label=sub_doc.id)    
              with sub_expander:
                st.write(f'{sub_doc.id} => {sub_doc.to_dict()}')
    except KeyError:
      st.error('Stages cannot be left empty')
  


      

    


 

        


  
                

