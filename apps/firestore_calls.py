from google.cloud import firestore
import streamlit as st
import pandas as pd
import SessionState
import streamlit as st

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json('firestore-key.json')
session_state = SessionState.get(checkboxed=False)
session_state.checkboxed = False

y_n = ["Yes", "No"]

#For MoSCoW requirements : 
moscow = ['Should', 'Could', 'Would']

def get_docs(col, selected_model, subcol):
    
    document = db.collection(col).document(selected_model).collection(subcol)

    return document

def get_recommended_practices(sel_model, type_m_p , pipeline = False):

    recommendation_practices_pipeline = [] 

    recommendation_practices_all = []

    for req in moscow:

       req_list = get_requirements(req, sel_model)
        
       for dim in req_list:

        if pipeline == True: 
        
        
          #Here, you have a dicrtionary with all the model's pipeline activities 
          pipeline_list = get_model_pipeline(sel_model)
          
          #Method doc contains the actual methods that can be called by id, and to_dict
          method_dict = get_methods_pipeline(dim, pipeline_list, type_m_p, pipeline)

          #We want to make a query to get methods based on the pipeline activities as well
          for d in method_dict:
            recommendation_practices_pipeline.append(d)

        return recommendation_practices_pipeline

        if pipeline == False: 
          
          #Method doc contains the actual methods that can be called by id, and to_dict
          method_docs = get_methods_overall(dim, type_m_p, pipeline)

          #We want to display our method doc nicely under a beta expander
          for doc in method_docs:

            recommendation_practices_all.append(doc.to_dict())
        
        return recommendation_practices_all
      

def get_requirements(req, sel_model):
      
      reqs_dim = []

      #Locate to the colelction where fairness requirements are specified for the particular model 
      fair_doc = db.collection("Models", sel_model, "Fairness Requirements").where(u'Requirement', u'==', req).stream()
      
      for f in fair_doc:

        # f.id is the name of your document

        # store these names in a list
        reqs_dim.append(f.id)

      return reqs_dim 

def get_methods_pipeline(dim, pipeline_list, type_m_p, pipeline = True):
    #Store methods into a dictionary 
    dim_dict = {}

    if pipeline == True: 
      
      for pipeline_stage in pipeline_list:
        
        method_doc = db.collection(type_m_p).where(u'Dimension', u'==', dim).where(u'Pipeline', u'==', pipeline_stage).stream()

        for doc in method_doc:
        
            dim_dict[pipeline_stage] = doc.to_dict()

      return dim_dict
      

def get_methods_overall(dim, type_m_p, pipeline = False):
    #Store methods into a dictionary 
    dim_dict = {}

    if pipeline == False:
      
      #use this list to get the methods from firestore
      method_doc = db.collection(type_m_p).where(u'Dimension', u'==', dim).stream()
    
      return method_doc

def get_model_pipeline(sel_model):

    #Create list for model pipeline 
    m_pipeline = {}
    
    model_pipeline = db.collection("Models", sel_model, "Technical Information").document("Pipeline").get()

    for doc in model_pipeline:

      st.write(doc.to_dict())

    return model_pipeline_dict

def set_model_requirements(sel_model, social_fairness_notion, scale):

    model_req = db.collection("Models").document(sel_model).collection("Fairness Requirements").document(social_fairness_notion)
    doc_req = db.collection(social_fairness_notion)
    i = 0

    values = []

    for doc in doc_req.stream():
        doc_r = doc.to_dict();
        name = doc_r.get("Name")
  	       
        with st.form(key=doc.id):
          answer = {}

          val = st.selectbox(name, scale)
          answer = val          

          submitted = st.form_submit_button('Submit')
            
          if submitted:
            st.write('You have successully set ' + name + ' as ' + answer + ' !' )
            model_req.update({doc.id : answer})

#Set technical pipeline for model 

def set_model_technical_requirements(sel_model, technical_component, query_point):

  model_pipeline = db.collection("Models", sel_model, "Technical Information").document("Pipeline").update({query_point: technical_component})

# Recommendations via Querying

#Mapping from Lee2020 (Inequalities -> Philosophy)
def get_model_philosophies(sel_model):

    #Create list for model pipeline 
    recommended_philosophies = []
    
    model_inequalities = db.collection("Models").document(sel_model).collection("Fairness Requirements").document("Fairness Inequalities")

    model_inequalities_dict = model_inequalities.get().to_dict();

    for k in model_inequalities_dict.keys():
      method_doc = db.collection("Fairness Philosophies").where(u'supported_inequalities', u'array_contains', k).stream()
      
      for d in method_doc:
        #st.write("Recommendations :", d.id)
        recommended_philosophies.append(d.to_dict())

    return recommended_philosophies


#Mapping from Lee2020 (Philosophy -> Definitions)
def get_model_definitions(sel_model):
    
    recommendations_definitions = []

    model_inequalities = db.collection("Models").document(sel_model).collection("Fairness Requirements").document("Fairness Philosophies")

    model_inequalities_dict = model_inequalities.get().to_dict();

    for k in model_inequalities_dict.keys():
      method_doc = db.collection("Fairness Definitions").where(u'fairness_philosophy', u'==', k).stream()

      for d in method_doc:
        
        name = d.get("Name")
        description = d.get("fairness_philosophy")

        recommendations_definitions.append(name, description)
    
    return recommendations_definitions

#Get data 
def get_notions(social_fairness_notion):

  fairness_notion_array = []

  fairness_notion = db.collection(social_fairness_notion)

  fairness_notion_docs = fairness_notion.stream();

  for d in fairness_notion_docs:
    d_dict = d.to_dict()
    name = d_dict.get("Name")
    fairness_notion_array.append(name)
  
  return fairness_notion_array

#Technical Mitigation Methods 

def get_technical(technical_component):

  technical_dict = {}

  technical_notion = db.collection(technical_component)

  technical_notion_docs = technical_notion.stream();

  for d in technical_notion_docs:
    
    d_dict = d.to_dict()

    id_dict = d_dict.get("id")

    technical_dict[d.id] = id_dict

  return technical_dict

def get_technical_query(technical_component, query_object, query_point):

  technical_array = []

  technical_notion = db.collection(technical_component)

  technical_notion_docs = db.collection(technical_component).where(query_object, u'==', query_point).stream()

  for d in technical_notion_docs:
    #d_dict = d.to_dict()
    technical_array.append(d.id)
  
  return technical_array

#Pagination


def pagination(data, b1, b2, mode = "Explore Recommendations"):

    page_length_max = len(data)

    st.write(
        f"""
        ##### {mode}
        """
    )
    st.write("")
    if "page" not in st.session_state:
        st.session_state.page = 0

    def next_page():
        st.session_state.page += 1

    def prev_page():
        st.session_state.page -= 1

    col1, col2, col3, _ = st.columns([0.1, 0.17, 0.1, 0.63])

    if st.session_state.page < (page_length_max - 1):
        col3.button(">", on_click=next_page, key=b1)
    else:
        col3.write("")  # this makes the empty column show up on mobile

    if st.session_state.page > 0:
        col1.button("<", on_click=prev_page, key=b2)
    else:
        col1.write("")  # this makes the empty column show up on mobile

    col2.write(
      
      f"""
        ###### Page {1+st.session_state.page} of {page_length_max}
      """
    )

    start = 1 * st.session_state.page
    end = start + 1

    for i in data[start:end]:
        st.write(f"""
          ###### {i   
            }
        """
        )








