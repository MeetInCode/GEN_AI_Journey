from dotenv import load_dotenv 
load_dotenv() #loading all the environment variables from .env file

import os
from PIL import Image
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel("gemini-1.5-flash")
chat=model.start_chat(history=[])

def get_response(input):
    response = chat.send_message(input,stream=True)
    return response


# Streamlit app
st.set_page_config(page_title="QA demo", page_icon=":rocket:")
st.header("Gemini flash Chatbot")

#initialize session state for chat history if it doesnt exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_area("Enter your prompt here", key="input")
submit = st.button("Generate")

if submit and input:
    response = get_response(input)
    # add the user input and response to the streamlit session chat history
    st.session_state['chat_history'].append(("you",input))
    st.subheader("The response is:")
    for chunk in response:
        st.write(chunk.text, end="")
       
    st.session_state['chat_history'].append(("Bot",response.text))

st.subheader("Chat History")

for speaker, text in st.session_state['chat_history']:
    if speaker == "you":
        st.write(f"User: {text}")
    else:
        st.write(f"Bot: {text}")