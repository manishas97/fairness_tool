from multiapp import MultiApp
from apps import interactive_guide, home
import streamlit as st

app = MultiApp()
# Add all your application here

app.add_app("Home", home.app)
#app.add_app("General Awareness", awareness)
#app.add_app("Dilemmas", interactive_guide.app)
#app.add_app("Model Information", pipeline.app)
#app.add_app("Perspectives", model_perspective.app)
#app.add_app("Explore fairness", model_owner_mode.app)
#app.add_app("Explore technical mitigation methods for fairness", model_developer.app)
#app.add_app("Interface", interface.app)
# The main app
app.run()
