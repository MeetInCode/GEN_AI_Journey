from dotenv import load_dotenv 
load_dotenv() #loading all the environment variables from .env file

import os
import numpy
import pandas 
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

#function to load gemini pro mdel and get responses

model = genai.GenerativeModel("gemini-1.5-flash")
def get_gemini_pro_response(prompt):
   response = model.generate_content(prompt)
   return response.text 


st.set_page_config(page_title="Gemini Pro", page_icon=":rocket:")
st.header("Gemini Pro")

input = st.text_area("Enter your prompt here", key="prompt")
submit = st.button("Generate")

#when submit is clicked 

if submit:
   response = get_gemini_pro_response(input)
   st.subheader("Response")
   st.write(response)