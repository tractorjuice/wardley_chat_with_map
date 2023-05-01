# Importing required packages
import streamlit as st
import requests
from streamlit_chat import message
import openai

API_ENDPOINT = "https://api.onlinewardleymaps.com/v1/maps/fetch?id="
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
model = "gpt-4"

html_temp = """
                <div style="background-color:{};padding:1px">
                
                </div>
                """

st.set_page_config(page_title="Chat with your Wardley Map")
st.sidebar.title("Chat with Map")
st.sidebar.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.1.4")
st.sidebar.markdown("Using GPT-4 API")
st.sidebar.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
st.sidebar.markdown("## Enter Map ID")
    
def get_initial_message():
    query = "Suggest some questions you can answer about this Wardley Map?"
    url = f"https://api.onlinewardleymaps.com/v1/maps/fetch?id={map_id}"
    response = requests.get(url)
    map_data = response.json()
    map_text = map_data["text"]
    st.session_state['map_text'] = map_text
    
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

if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    
if 'map_text' not in st.session_state:
    st.session_state['map_text'] = []
    
query = st.text_input("Question: ", value="", key="input")
    
map_id = st.sidebar.text_input("Enter the ID of the Wardley Map:", value="7OPuuDEWFoyfj00TS1")
st.sidebar.write("For https://onlinewardleymaps.com/#clone:OXeRWhqHSLDXfOnrfI")
st.sidebar.write("Examples:\n\ngQuu7Kby3yYveDngy2\n\nxi4JEUqte7XRWjjhgQ\n\nMOSCNj9iXnXdbCutbl\n\nOXeRWhqHSLDXfOnrfI")
st.sidebar.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    
if st.session_state.get('current_map_id') != map_id:
    del st.session_state['messages']
    st.session_state['past'] = []
    st.session_state['generated'] = []
    st.session_state['current_map_id'] = map_id
    query = "Suggest some questions you can answer about this Wardley Map?"
    st.session_state['messages'] = get_initial_message()
    
title = ""

if 'map_text' in st.session_state:
    st.sidebar.markdown("### Downloaded Map Data")
    map_text = st.session_state['map_text']
    for line in map_text.split("\n"):
        if line.startswith("title"):
            title = line.split("title ")[1]
    if title:
        st.sidebar.markdown(f"### {title}")
    st.sidebar.write(st.session_state['map_text'])

if query:
    with st.spinner("generating..."):
        #map_data = st.session_state['map_text']
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        response = get_chatgpt_response(messages, model)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)
        del st.session_state["input"]

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
