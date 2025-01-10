from dotenv import load_dotenv 
load_dotenv() #loading all the environment variables from .env file

import os
from PIL import Image
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_pro_response(input, image):
    if input != "":
        response = model.generate_content([input, image])
        return response.text
    else:
        response = model.generate_content([image])
        return response.text

# Streamlit app

st.set_page_config(page_title="Gemini Pro Vision", page_icon=":rocket:")
st.title("Gemini Pro Vision")

input_text = st.text_input("Enter your input text:",key="input")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if st.button("Generate Response"):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True) 
        response = get_gemini_pro_response(input_text, image)
        st.write(response)
    else:
        st.write("Please upload an image.")