import streamlit as st
import pandas as pd

st.title('Enter model information')
@st.cache(allow_output_mutation=False)
def record_app_domain():
  return {}

@st.cache(allow_output_mutation=True)
def record_app_tech():
  return {}

def model_name():
  st.write('blah blah')

def app_domain():

  app_domain_options = ("Customer Service","Commercial lending operations", "Letter of credit and guarantees", 
                "Banking Regulatory and Compliance", "Import and Export Payments", "Payment investigations and repair")
  app_domain = st.selectbox('Select model domain', options = app_domain_options, index=0, key = 4)

  return app_domain

def app_tech():
  
  app_tech = ("Natural Language Processing","Machine Learning","Deep Learning", "Crowd computing", "Information Retrieval")
  app_tech = st.selectbox('Select the primary technology', options = app_tech, index=0, key = 5)


def display_fnfp(domain):

  loan = 'Commercial lending operations'
  if domain ==loan:
    st.markdown('A false positive means the following : A consumer **IS GRANTED** a loan but is not probable to pay it back.')
    st.markdown('A false negative means the following ; A consumer is **NOT GRANTED** a loan but is probable to pay it back if they were granted the loan.')


def display_fairness_metrics(domain):
  
  loan = 'Commercial lending operations'
  
  if domain == loan:
    st.markdown('Please pay extra attention to understand the following concepts:')

    col1, col2, col3 = st.beta_columns([.5,.5,.5])
    button_dp = col1.button("Demographic Parity")
    button_rf = col2.button("Rawlsian Fairness")
    button_eo = col3.button("Equal Opportunity")
    
def information_capacity(domain):
  ic = []
  ic_1_options = ['No', 'Possibily','Yes']
  ic_2_options = ['No', 'Possibily','Yes']
  ic_3_options = ['False Negative', 'False Positive']
  ic_4_options = ['No', 'Possibly','Yes']
  ic_5_options = ['No', 'Possibly','Yes']
  
  ic_1 = st.select_slider('Do you have access to sensitive information if model is in development', options= ic_1_options , key=10)
  ic_2 = st.select_slider('Do you have access to sensitive information if model is in production', options= ic_2_options , key=11)
  ic_3 = st.select_slider('Is a false negative or false positive worse?',  options= ic_3_options, key=12)
  display_fnfp(domain)
  ic_4 = st.select_slider('Do you need to provide a justification to the client?',  options= ic_4_options , key=13)
  ic_5 = st.select_slider('Does this process have human reviewals or decision making in combination with the model?',  options= ic_5_options , key=14)

  ic.append(ic_1)
  ic.append(ic_2)
  ic.append(ic_3)
  ic.append(ic_4)
  ic.append(ic_5)
  
  return ic

@st.cache(allow_output_mutation=True)
def sensitive_attributes():
  return []

def model_information():
  st.header('Please enter some information about the model')
  path = st.text_input('What is considered as sensitive information/attributes for this model?')
  
  col1, col2 = st.beta_columns([.5,4])
  button_save = col1.button("Save")
  button_reset = col2.button("Reset")

  if button_reset:
    sensitive_attributes().clear()

  if button_save:
    sensitive_attributes().append(path)
    s_a = sensitive_attributes();
    st.dataframe(s_a)

def display_info():
  st.write('Recommended because you selected NO sensitive attributes')

  col1,col2,col3 = st.beta_columns([.5,.5,.5])
  col4,col5,col6 = st.beta_columns([.5,.5,.5])
    
  button_des = col1.button('Description of Rawlsian Fairness')
  button_ad = col2.button('Advantages and Disadvantages')
  button_fp = col3.button('Relevant Fairness Practices')
  button_tm = col4.button('Relevant technical methods')
  button_si = col5.button('Understand Social Implications')
  button_csl = col6.button('Case Studies (Literature/User input)')

def app():
  st.title('Guide')

  domain = app_domain();

  app_tech();

  model_information();

  information_capacity(domain);
  
  button_cal = st.button("Calculate")

  if button_cal:
    display_fairness_metrics(domain); 
  
  button_smi = st.button("Show more information")

  if button_smi:
    display_info();


  

     


  




  
  


  
    
    