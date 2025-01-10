from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GENAI_API_KEY'))

#function to load gemini flash model

model=genai.GenerativeModel('gemini-1.5-pro')
def get_gemini_response(input,image,prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

# The image_details function in InvoiceExtractor.py processes an uploaded image file by extracting its binary data and MIME type, then returns this information in a list of dictionaries. This data is used later to generate a response from a generative model when the user submits a prompt and an image through the Streamlit interface

def image_details(uploaded_fle):
    if uploaded_fle is not None:
        bytes_data = uploaded_fle.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_fle.type,
                "data": bytes_data
            }
        ]
        #look below to see what this will return 
        return image_parts
    else:
        return None

#streamlit setup

st.set_page_config(page_title="Invoice Extractor", page_icon=":rocket:")
st.header("Invoice Extractor")
input = st.text_area("Enter your prompt here", key="input")
uploaded_fle = st.file_uploader("Choose an image...", type=["jpg","png","jpeg"])
#open pdf anddisplay image
image=""
if uploaded_fle is not None:
    image = Image.open(uploaded_fle)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

submit = st.button("Tell Me About This Invoice")

input_prompt = """
you are an expert in understanding and analyzing invoices.we will upload an invoice image and you will answer questions based on the uploaded invoice image.
"""

#if submit button is clicked
if submit:
    image_details_array = image_details(uploaded_fle)
    response = get_gemini_response(input_prompt,image_details_array,input)
    st.subheader("The response is:")
    st.write(response)
else:
    st.write("Please upload an image to get started")


# """
# [
# 0:{
# "mime_type":"image/png"
# "data":"b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x03\xd4\x00\x00\x04\x96\x08\x06\x00\x00\x00\xcb\xe3\xe4m\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00 \x00IDATx\x9c\xec\xddwx\x14\xd5\xde\x07\xf0\xef\xecnz\x0f\t\xa4\xd0!4)R\x95 \x84\xae\x14\xb1\x804\x11\xbb\x88\xd2\xe4"X\xde\xeb\xb5 \x16\x14\x04A\x04\x1b\x02rQ\x10\x1b\n\x88\xf4\x16\x12z\x0f=\t-!\xa4\xf7\xec\xeey\xff\x08;wg7[\xb2\xd9MB\xf8~\x9eg\x1f2s\xce\x9c93\x1b\xb2\xfb\x9b\xd3\xa4\xae\xd1\xdd\x85\x1
# }]
# """
