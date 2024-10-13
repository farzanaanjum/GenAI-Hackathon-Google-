from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import json
import google.generativeai as genai
import requests
from streamlit_lottie import st_lottie  

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Animation files
lottie_coding1 = load_lottiefile("lottiefiles/coding1.json")  
lottie_coding2 = load_lottiefile("lottiefiles/coding2.json")

# Initialize our Streamlit app
st.set_page_config(page_title="DSA")

# Create two columns for the logo and header
logo_col, header_col = st.columns([1, 5])  

with logo_col:
    st_lottie(
        lottie_coding2,
        speed=1,
        reverse=False,
        loop=True,
        quality="low", 
        height=100,  
        width=100,   
        key="logo",
    )

with header_col:
    # Display the header next to the logo
    st.header("DSA Socratic Teaching Assistant")

# Create two columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    # Initialize session state for chat history 
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    input = st.text_input("Prompt ", key="prompt")
    submit = st.button("Generate")

    if submit and input:
        response = get_gemini_response(input)
        # Add user query and response to session state chat history
        st.session_state['chat_history'].append(("You", input))
        st.subheader("The Response is")
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))

    st.subheader("The Chat History")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

with col2:
    st_lottie(
        lottie_coding1,  
        speed=1,
        reverse=False,
        loop=True,
        quality="low",  # medium ; high
        height=None,
        width=None,
        key=None,
    )
