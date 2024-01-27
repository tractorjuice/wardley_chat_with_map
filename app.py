# Importing required packages
import streamlit as st
import requests
import openai
import promptlayer
import requests

API_ENDPOINT = "https://api.onlinewardleymaps.com/v1/maps/fetch?id="
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
promptlayer.api_key = st.secrets["PROMPTLAYER"]

# gpt-3.5-turbo, gpt-4, and gpt-4-turbo-preview point to the latest model version
#MODEL = "gpt-3.5-turbo" # 4K, Sept 2021
MODEL = "gpt-3.5-turbo-16k" # 16K, Sept 2021
#MODEL = "gpt-3.5-turbo-1106" # 16K, Sept 2021
#MODEL = "gpt-4" # 8K, Sept 2021
#MODEL = "gpt-4-32k" # 32K, Sept 2021
#MODEL = "gpt-4-turbo-preview" # 128K, Apr 2023
#MODEL = "gpt-4-1106-preview" # 128K, Apr 2023

DEBUG = True # True to overwrite files that already exist

# Swap out your 'import openai'
openai = promptlayer.openai

st.set_page_config(page_title="Chat with your Wardley Map")
st.sidebar.title("Chat with Map")
st.sidebar.divider()
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.1.5")
st.sidebar.markdown("Using gpt-3.5-turbo-16k API")
st.sidebar.divider()
st.sidebar.markdown("## Enter Map ID")

def get_map_data(map_id):
    url = f"{API_ENDPOINT}{map_id}"
    response = requests.get(url)
    map_data = response.json()
    map_text = map_data["text"]
    return map_text

map_id = st.sidebar.text_input("Enter the ID of the Wardley Map:", value="OXeRWhqHSLDXfOnrfI")
st.sidebar.write("For https://onlinewardleymaps.com/#clone:OXeRWhqHSLDXfOnrfI")
st.sidebar.write("Examples:\n\ngQuu7Kby3yYveDngy2\n\nxi4JEUqte7XRWjjhgQ\n\nMOSCNj9iXnXdbCutbl\n\nOXeRWhqHSLDXfOnrfI\n\nO42FCNodPW3UPaP8AD")
st.sidebar.divider()

if 'map_text' not in st.session_state:
    st.session_state['map_text'] = get_map_data(map_id)
    
if st.session_state.get('current_map_id') != map_id:
    st.session_state['current_map_id'] = map_id
    query = "Suggest some questions you can answer about this Wardley Map?"
    st.session_state['map_text'] = get_map_data(map_id)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
            "role": "system",
            "content": f"""
             As a chatbot, analyze the provided Wardley Map and offer insights and recommendations based on its components.

             Suggestions:
             Request the Wardley Map for analysis
             Explain the analysis process for a Wardley Map
             Discuss the key insights derived from the map
             Provide recommendations based on the analysis
             Offer guidance for potential improvements or adjustments to the map
             WARDLEY MAP: {st.session_state['map_text']}
             """
        })
    st.session_state.messages.append(   
        {
            "role": "user",
            "content": "Suggest some questions you can answer about this Wardley Map?"

        })
    st.session_state.messages.append(
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
        })
    
title = ""

if 'map_text' in st.session_state:
    st.sidebar.markdown("### Downloaded Map Data")
    map_text = st.session_state['map_text']
    for line in map_text.split("\n"):
        if line.startswith("title"):
            title = line.split("title ")[1]
    if title:
        st.sidebar.markdown(f"### {title}")
    st.sidebar.code(st.session_state['map_text'])

for message in st.session_state.messages:
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if query := st.chat_input("Ask a question about this map?"):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
            pl_tags=["chatwithmap"]
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
