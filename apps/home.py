from google.cloud import firestore
import SessionState
import streamlit as st
import pandas as pd
from apps import create_your_pipeline, model_owner, model_developer as md
from apps import toc
import random
import time


# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json('firestore-key.json')
session_state = SessionState.get(checkboxed=False)
session_state.checkboxed = False


def display_models(Names):
    # And then render each post, using some light Markdown
    models_list = db.collection("Models")

    for doc in models_list.stream():
        model = doc.to_dict()
        Name = model["id"];
        Description = model["description"];
        Names.append(Name);

    Names.append("Add new model")
    selected_model = st.sidebar.selectbox("Model", Names)

    return selected_model


def add_new_model(Names):

    # Streamlit widgets to let a user create a new post
    name = st.sidebar.text_input("Enter the model name")
    model_description = st.sidebar.text_input("Enter model description")
    submit = st.sidebar.button("Create new model")

    # Once the user has submitted, upload it to the database
    if (name and model_description and submit):
        doc_ref = db.collection("Models").document(name)

        doc_ref.set({
            "id": name,
            "description": model_description
        })

    return True

@st.cache(allow_output_mutation=True)
def set_role(role):
    return role

@st.cache(allow_output_mutation=True)
def set_model(model):
    return model

@st.cache(allow_output_mutation=True)
def set_button(button):

    if button == True:
        print = "Your model is set successfully as "

    else:
        print = "Please set your model by clicking the button 'Set your model' "

    return print, button

def stream_info_database(coll, subcollection, docu):

    doc_model = db.collection(coll).document(docu).collection(subcollection);

    for doc in doc_model.stream():
        df = doc.to_dict();

    return df

def select_model(selected_model, Names):

    if (selected_model == "Add new model"):
        add_new_model(Names);
        if (add_new_model == True):
            display_models(Names)

    else:
        doc_model = db.collection("Models").document(selected_model)
        model_information = doc_model.get()
        model_info = model_information.to_dict()
        #st.write(model_info["description"])
        selected_model_button = st.sidebar.button("Set your model")

        return selected_model_button


def app():

    #Variables
    Names = []

    #Selection the model for this session

    st.sidebar.subheader("Choose your model")
    st.sidebar.write("If your model name is not in the list, please add a new model")

    #Display the models list
    selected_model = display_models(Names)

    #Cache selected model name
    selected_model = set_model(selected_model)

    #Recursive method to either add new model or select a model name from the updated list
    selected_model_button = select_model(selected_model, Names)

    #Cache if model was "Set" using the button,
    #returns print statement for user indicated success/failure to set model
    #print_model_set= set_button(selected_model_button)

    #If Model was set, or session state is preserved
    if selected_model_button:
       session_state.checkboxed = True
       # Print the statement for user indicating success/failure to set model
       st.write("Set successfully to ", selected_model)

    if selected_model_button or session_state.checkboxed:

       #Ask them to indicate their role, role is already cached in method get_role

       role = get_role();

       #if fairness_requirements_mo or session_state.checkboxed:
       if role == "Model Owner":
            fairness_requirements_mo = st.sidebar.checkbox("Indicate fairness requirements")                    
            
            if fairness_requirements_mo:
              st.write(" Do you want to specify the relevant social fairness notions?")
              explore_fairness = st.checkbox("Specify fairness notions")
              
              if explore_fairness:
                model_owner.exploration(selected_model);
                model_owner.recommendation(selected_model);
              
              st.write("Specify your fairness definitions! If you have already specified social fairness notions, you can see recommendations!")

              set_fairness = st.checkbox("Specify fairness definitions")

              if set_fairness:

                 model_owner.explore_definitions(selected_model);

              st.write("Have you already set the fairness notions, and want to re-visit them?")

              revisit_fairness = st.checkbox("Re-visit fairness notions")

              
       if role == "Model Developer":
            show_fairness_reqs_bt = st.sidebar.checkbox("Show social context and fairness")
            
            st.sidebar.write("Do you wish to view the pipeline of this model?")

            display_pipeline = st.sidebar.checkbox("See pipeline of " + selected_model)

            if show_fairness_reqs_bt:
              show_fairness_reqs(selected_model)   


            if display_pipeline:

              #Show your pipeline
              st.write("This is the current model pipeline")
              
              md.get_activities(selected_model)

              #display_pipeline(pipeline)

              st.write("Do you wish to adjust the pipeline of this model?")
            
              add_to_pipeline = st.checkbox("Add to pipeline of " + selected_model)

              if add_to_pipeline:
                md.select_activities(selected_model)
                md.add_activities(selected_model)
              
              #Explore mitigation methods

              st.write("Do you wish to review technical fairness mitigations methods for the pipeline of this model?")

              explore_pipeline_bt = st.sidebar.checkbox("Explore technical mitigation methods")                    
              
              if explore_pipeline_bt:
                md.recommendations_methods(sel_model = selected_model, type_m_p='Methods')
  

def get_role():

    #Variables of roles
    roles = ["Model Owner", "Model Developer", "Domain Expert"]

    st.sidebar.subheader("Enter your role")

    #Select box for displaying the roles
    role = st.sidebar.selectbox("Select your role", options=roles)

    #Cache this
    role = set_role(role);

    return role

@st.cache(allow_output_mutation=True)
def return_select_slider(vv):
    return vv


def show_fairness_reqs(selected_model):
    
    fairness_types = ["Procedural", "Distributive"]
    
    for f in fairness_types:
      st.write(f)
      my_expander = st.beta_expander(label='Click for more information')
      doc_fair_reqs = db.collection("Models").document(selected_model).collection("Fairness Requirements").document(f)
      d = doc_fair_reqs.get()
      doc = d.to_dict()
      use_case = {}
      for i, v in doc.items():
        if i == 'Use Cases':
          use_case[i] = v
          doc.pop(i)
          break;
      df = pd.DataFrame.from_dict(doc, orient='index', columns=['Requirement'])
      with my_expander:
        st.write(df)
        st.write(use_case)
    

def show_tech_model_info(selected_model):

    collection = "Models"
    document = selected_model
    subcollection_1 = "Technical Information"
    subcollection_2 = "Fairness Requirements"

    subsubcollection = "Components"

    technical_info_model = stream_info_database(collection, subcollection_1, document)

    pipeline = []
    fr_info_model = stream_info_database(collection, subcollection_2, document)

    for doc in technical_info_model:
        pipeline.append(doc)
      
    return pipeline 
        









 

