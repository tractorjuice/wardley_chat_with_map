# Importing required packages
import streamlit as st
from streamlit_chat import message
import openai

st.set_page_config(page_title="Chat with WardleyGPT")
st.title("Chat with WardleyGPT")
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.1.4")
st.sidebar.markdown("Using GPT-4 API")
st.sidebar.markdown("Not optimised")
st.sidebar.markdown("May run out of OpenAI credits")

API_ENDPOINT = "https://api.onlinewardleymaps.com/v1/maps/fetch?id="
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
model = "gpt-4"

def get_initial_message():
    messages=[
            {"role": "system", "content": """
             As a chatbot, analyze the provided Wardley Map and offer insights and recommendations based on its components.
             Suggestions:
             Request the Wardley Map for analysis
             Explain the analysis process for a Wardley Map
             Discuss the key insights derived from the map
             Provide recommendations based on the analysis
             Offer guidance for potential improvements or adjustments to the map
             WARDLEY MAP: {map}
             QUESTION: {question}
             YOUR RESPONSE:
             Provide your answers using Wardley Mapping in a form of a sarcastic tweet.
             """},
            {"role": "user", "content": ""},
            {"role": "assistant", "content": ""}
        ]
    return messages

def get_chatgpt_response(messages, model=model):
    print("model: ", model)
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages
    )
    return response['choices'][0]['message']['content']

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
    
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_input("Question: ", "What questions can I ask about this Wardley Map?", key="input")

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()

if query:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        response = get_chatgpt_response(messages, model)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
