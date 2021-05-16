import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from textblob import TextBlob
from nltk.tokenize import sent_tokenize
from gensim.summarization.summarizer import summarize 
from gensim.summarization import keywords
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()


def activity():
  NLP_activity = ('Text summarization', 'Entity Recognition', 'Sentiment Analysis', 'Spam Filtering', 'Speech Synthesis', 'Speech Recognition')
  sub_activity = st.selectbox('Select sub-activity', NLP_activity, key = 30)

  return sub_activity

def text():
  st.write('Enter the text you would like to analyze')
  text = st.text_input('Enter text here')

  return text

def entRecognizer(entDict, typeEnt):
  ent_list = [ent for ent in entDict if entDict[ent] == typeEnt]
  return ent_list

def entity_recognition(input_text):
    entities = []
    entityLabels = []
    doc = nlp(input_text)
    
    for ent in doc.ents:
        entities.append(ent.text)
        entityLabels.append(ent.label_)

    entDict = dict(zip(entities, entityLabels)) #Creating dictionary with entity and entity types

    #Using function to create lists of entities of each type
    entOrg = entRecognizer(entDict, "ORG")
    entCardinal = entRecognizer(entDict, "CARDINAL")
    entPerson = entRecognizer(entDict, "PERSON")
    entDate = entRecognizer(entDict, "DATE")
    entGPE = entRecognizer(entDict, "GPE")

    #Displaying entities of each type
    st.write("Organization Entities: " + str(entOrg))
    st.write("Cardinal Entities: " + str(entCardinal))
    st.write("Personal Entities: " + str(entPerson))
    st.write("Date Entities: " + str(entDate))
    st.write("GPE Entities: " + str(entGPE))

def dist_over_acc():
  enfc = ENFC(input_text)


def app():
  st.write('NLP Pipeline')
  sub_activity = activity();
  if sub_activity=='Entity Recognition':
    my_text = text();
    st.write('Using Spacy')
    entity_recognition(my_text);

    st.write('Using GloVe')
    
