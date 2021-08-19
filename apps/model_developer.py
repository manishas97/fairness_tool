import streamlit as st
import pandas as pd
import collections
import os
import technical_data
import utils
from apps import firestore_calls as fc

path = '/content/drive/MyDrive/fairness_tool/technical_data'

template_dict = collections.defaultdict(dict)
template_dirs = [
    f for f in os.scandir(path) if f.is_dir() and f.name != ".ipynb_checkpoints"]
# TODO: Find a good way to sort templates, e.g. by prepending a number to their name
#   (e.g. 1_Image classification_PyTorch).
template_dirs = sorted(template_dirs, key=lambda e: e.name)
for template_dir in template_dirs:
    try:
        # Templates with task + framework.
        task, framework = template_dir.name.split("_")
        template_dict[task][framework] = template_dir.path
    except ValueError:
        # Templates with task only.
        template_dict[template_dir.name] = template_dir.path
# print(template_dict)

def recommendations_methods(sel_model, type_m_p):

    st.info(
        "Select a mode to find the relevant fairness definitions and metrics for the" 
        + sel_model + "Model"
    )

    st.write("## Select model")

    task = st.radio(
        "Which mode do you want to view the recommendations?  ", list(template_dict.keys())
    )
    if isinstance(template_dict[task], dict):
        framework = st.selectbox(
            "In which framework?", list(template_dict[task].keys())
        )
        template_dir = template_dict[task][framework]
    else:
        template_dir = template_dict[task]


    # Show template-specific sidebar components (based on sidebar.py in the template dir).
    template_sidebar = utils.import_from_file("template_sidebar", os.path.join(template_dir, "sidebar.py"))
    template_sidebar.show(sel_model, type_m_p)

# Display current activities in stages from pipeline 


def get_activities(sel_model):

  pipeline = fc.get_model_pipeline(sel_model)

  st.write(pipeline)
  #fc.pagination(pipeline, "pipeline_bt1", "pipeline_bt2")

# Select activitites to stages to design pipeline, by model developer 

def select_activities(sel_model):
  
  stages_dict = fc.get_technical("Stages")

  i = 0
  
  alpha_array = ['i', 'j', 'k', 'l', 'm', 'n', 'o']
  
  for stage, stage_id in stages_dict.items():
    
    st.write(stage)

    activities_array = fc.get_technical_query("Components", "Stage", stage_id)

    # Streamlit widgets to let a user create a new post
    selected_activities = st.multiselect('Select relevant activities', activities_array, key = stage_id)

    submit = st.button("Submit selected activities", key = alpha_array[i])

    i = i + 1
    # Once the user has submitted, upload it to the database
    if submit:
      
      for activity in selected_activities:
        
        fc.set_model_technical_requirements(sel_model, activity, stage_id)

        st.write("Successfully added " + activity + " to " + sel_model + " pipeline!")
# Add new activities to firebase
  
def add_activities(sel_model):
  
  st.write('Do you want to add an activity?')

  stages_array = fc.get_technical("Stages")

  # Streamlit widgets to let a user create a new post
  name = st.text_input("Name your activitity")
  description = st.text_input("Add description")
  stage = st.multiselect('Assign a stage', stages_array, key="add_activity")

  submit = st.button("Submit new activity", key = "add_activity_bt")

  # Once the user has submitted, upload it to the database
  if name and description and stage and submit:
    doc_ref = db.collection("Components").document(name)
    doc_ref.set({"Description": description, "Stage": stage})

  
  


