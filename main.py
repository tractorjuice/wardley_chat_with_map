import streamlit as st
import requests
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

API_ENDPOINT = "https://api.onlinewardleymaps.com/v1/maps/fetch?id="
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
model = "gpt-4"

template = """
Your goal is to provide assistance on wardley maps and always give a verbose answer.
The input format for the provided Wardley Map a text description. The chatbot can be designed to handle any of these formats.
The main features or functionalities the chatbot should have can include explaining the different components and activities of the map, identifying patterns or potential improvements, offering insights and recommendations, and answering questions related to the map. For example, the chatbot can help users identify components that are in the commodity stage and suggest ways to reduce costs or improve efficiency. The chatbot can also help users identify components that are in the genesis stage and suggest ways to innovate and differentiate from competitors.
To help users understand the analysis better, the chatbot can provide examples or case studies. For example, the chatbot can show how other companies have used Wardley Maps to make strategic decisions or improve their systems. The chatbot can also provide tips and best practices for creating and analyzing Wardley Maps.
WARDLEY MAP: {map}
QUESTION: {question}
YOUR RESPONSE:
"""
def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    llm = OpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY, max_tokens=500)
    return llm

# Define the Streamlit app
def app():

    # Set the page title and layout
    st.set_page_config(page_title="Chat with your map")
    st.title("Chat with your map")
    st.sidebar.markdown("# Chat with your Wardley Map")
    st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
    st.sidebar.markdown("Current Version: 0.1.4")
        
    # Define the form to enter the map ID
    map_id = st.text_input("Enter the ID of the Wardley Map: For example https://onlinewardleymaps.com/#clone:OXeRWhqHSLDXfOnrfI, enter: OXeRWhqHSLDXfOnrfI", value="OXeRWhqHSLDXfOnrfI")
    question = st.text_input(label="Question ", value="Create a numbered list of the components in this wardley map.", key="q_input", max_chars=150)
    if len(question.split(" ")) > 700:
        st.write("Please enter a shorter question about your Wardley Map")
        st.stop()

    # Load the map data when the user submits the form
    if st.button("Ask Question to Wardley AI"):
        # Fetch the map data from the API
        url = f"https://api.onlinewardleymaps.com/v1/maps/fetch?id={map_id}"
        response = requests.get(url)

        # Check if the map was found
        if response.status_code == 200:
            map_data = response.json()
            
            prompt = PromptTemplate(
                input_variables=["map", "question"],
                template=template,
            )
                                    
            llm = load_LLM(OPENAI_API_KEY)
            
            prompt_wardley_ai = prompt.format(question=question, map=map_data)
            response = llm(prompt_wardley_ai)
            
            st.markdown("### Response:")
            st.write(response)
                   
        else:
            st.error("Map not found. Please enter a valid ID.")
                                                                                                                          
if __name__ == "__main__":
    app()
