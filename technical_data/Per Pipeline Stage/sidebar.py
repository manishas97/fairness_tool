import streamlit as st
from apps import firestore_calls as fc

def show(sel_model, type_m_p):
  
    """Shows the sidebar components for the template and returns user inputs as dict."""
    
    # `show()` is the only method required in this module. You can add any other code 
    # you like above or below. 
    
    inputs = {}  # dict to store all user inputs until return
    
    pipeline = True

    #with st.sidebar:
        
        # Render all template-specific sidebar components here. 
        
        # Store all user inputs in the `inputs` dict. This will be passed to the code
        # template later.
    
    #sel_model = ...
    #type_m_p = ...
    #pipeline = ...
    
    with st.beta_expander(label='Fairness Frameworks and Practices'):
      
      #Query the relevant practices based on the fairness requirements indicated by the model owner
      fc.get_recommended_practices(sel_model, type_m_p, pipeline = True);
     
    with st.beta_expander(label='Fairness Mitigation Methods'): 

      #Query the relevant mititgation methods based on the fairness requirements indicated by the model owner
      fc.get_recommended_practices(sel_model, type_m_p, pipeline = True);

  








