# Importing required packages
import streamlit as st
import requests
from streamlit_chat import message
import openai

st.set_page_config(page_title="Chat with WardleyGPT")
st.title("Chat with WardleyGPT")

# Define the form to enter the map ID
st.sidebar.markdown("### Wardley Map ID")
st.sidebar.markdown("")
map_id = st.sidebar.text_input("Enter the ID of the Wardley Map: For example https://onlinewardleymaps.com/#clone:OXeRWhqHSLDXfOnrfI, enter: OXeRWhqHSLDXfOnrfI", value="OXeRWhqHSLDXfOnrfI")

st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.1.4")
st.sidebar.markdown("Using GPT-4 API")

API_ENDPOINT = "https://api.onlinewardleymaps.com/v1/maps/fetch?id="
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
model = "gpt-4"

def get_initial_message():
    url = f"https://api.onlinewardleymaps.com/v1/maps/fetch?id={map_id}"
    response = requests.get(url)
    map_data = response.json()
    map_text = map_data["text"]
    messages = [
        {
            "role": "system",
            "content": f"""
             As a chatbot, analyze the provided Wardley Map and offer insights and recommendations based on its components.
             Suggestions:
             Request the Wardley Map for analysis
             Explain the analysis process for a Wardley Map
             Discuss the key insights derived from the map
             Provide recommendations based on the analysis
             Offer guidance for potential improvements or adjustments to the map
             Provide your answers using Wardley Mapping in a form of a sarcastic tweet.
             WARDLEY MAP: {map_text}
             """
        },
        {
            "role": "user",
            "content": "{question}"
        },
        {
            "role": "assistant",
            "content": """
            Here is a list of general questions that you could consider asking while examining any Wardley Map:
            1. What is the focus of this map - a specific industry, business process, or company's value chain?
            2. What are the main user needs the map is addressing, and have all relevant user needs been identified?
            3. Are the components correctly placed within the map based on their evolutions (Genesis, Custom Built, Product/Rental, Commodity)?
            4. What linkages exist between the components and how do they interact within the value chain?
             5. Can you identify any market trends or competitor activities that could impact the positioning of the components?
             6. Are there any potential inefficiencies or improvements that could be made in the value chain depicted in the map?
             7. How does your organization take advantage of upcoming opportunities or mitigate risks, considering the layout and components' evolutions on the map?
             8. Are there any areas where innovation or disruption could significantly alter the landscape represented in the map?
             It is essential to provide the actual Wardley Map in question to provide a more accurate, in-depth analysis of specific components or insights tailored to your map.
            """
        }
    ]
    return messages


def get_chatgpt_response(messages, model=model):
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
        
        url = f"https://api.onlinewardleymaps.com/v1/maps/fetch?id={map_id}"
        response = requests.get(url)
        map_data = response.json()
        
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
