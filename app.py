import streamlit as st
from multiapp import MultiApp
from apps import home, model_perspective, model, interactive_guide, heatmaps, pipeline, NLP_pipeline, create_your_pipeline # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Explore fairness in FinTech", pipeline.app)
app.add_app("A helpful Guide", interactive_guide.app)
app.add_app("Social Implications", heatmaps.app)
app.add_app("Record viewpoints", model_perspective.app)
app.add_app("Technical Detection NLP", NLP_pipeline.app)
app.add_app("Create your pipeline", create_your_pipeline.app)

# The main app
app.run()