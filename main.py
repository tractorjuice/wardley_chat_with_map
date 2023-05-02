# Importing required packages
import streamlit as st
import requests
from streamlit_chat import message
import openai
import json
import re
import requests

API_ENDPOINT = "https://api.onlinewardleymaps.com/v1/maps/fetch?id="
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
model = "gpt-4"

html_temp = """
                <div style="background-color:{};padding:1px">
                
                </div>
                """

def swap_xy(xy):
  new_xy = re.findall("\[(.*?)\]", xy)
  if new_xy:
    match = new_xy[0]
    match = match.split(sep = ",")
    match = match[::-1]
    new_xy = ('[' + match[0].strip() + ',' + match[1] + ']')
    return (new_xy)
  else:
    new_xy=""
    return (new_xy)

def parse_wardley_map(map_text):
    lines = map_text.strip().split("\n")
    title, evolution, anchors, components, nodes, links, evolve, pipelines, pioneers, market, blueline, notes, annotations, comments, style = [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
    current_section = None

    for line in lines:
        if line.startswith("//"):
            comments.append(line)

        elif line.startswith("evolution"):
            evolution.append(line)

        elif "+<>" in line:
            blueline.append(line)

        elif line.startswith("title"):
            name = ' '.join(line.split()[1:])
            title.append(name)

        elif line.startswith("anchor"):
            name = line[line.find(' ') + 1:line.find('[')].strip()
            anchors.append(name)

        elif line.startswith("component"):
            stage = ""
            pos_index = line.find("[")
            if pos_index != -1:
                new_c_xy = swap_xy(line)
                number = json.loads(new_c_xy)
                if 0 <= number[0] <= 0.17:
                    stage = "genesis"
                elif 0.18 <= number[0] <= 0.39:
                    stage = "custom"
                elif 0.31 <= number[0] <= 0.69:
                    stage = "product"
                elif 0.70 <= number[0] <= 1.0:
                    stage = "commodity"
                else:
                    visibility = ""
                if 0 <= number[1] <= 0.20:
                    visibility = "low"
                elif 0.21 <= number[1] <= 0.70:
                    visibility = "medium"
                elif 0.71 <= number[1] <= 1.0:
                    visibility = "high"
                else:
                    visibility = ""               
            else:
                new_c_xy = ""

            name = line[line.find(' ') + 1:line.find('[')].strip()

            label_index = line.find("label")
            if label_index != -1:
                label = line[label_index+len("label")+1:]
                label = swap_xy(label)
            else:
                label = ""

            components.append({"name": name, "description": "", "evolution": stage, "visibility": visibility, "positionxy": new_c_xy, "labelxy": label})

        elif line.startswith("pipeline"):
            new_c_xy = swap_xy(line)
            name = line[line.find(' ') + 1:line.find('[')].strip()
            pipelines.append({"name": name, "description": "", "positionxy": new_c_xy, "labelxy": ""})

        elif line.startswith("links"):
            links.append(line)

        elif line.startswith("evolve"):
            new_c_xy = swap_xy(line)
            name = re.findall(r'\b\w+\b\s(.+?)\s\d', line)[0]
            label_index = line.find("label")
            if label_index != -1:
                label = line[label_index+len("label")+1:]
            else:
                label = ""
            label = swap_xy(label)
            evolve.append({"name": name, "description": "", "positionxy": new_c_xy, "labelxy": label})

        elif line.startswith("pioneer"):          
            pioneers.append(line)

        elif line.startswith("note"):
            name = line[line.find(' ') + 1:line.find('[')].strip()
            pos_index = line.find("[")
            if pos_index != -1:
                new_c_xy = swap_xy(line)
            else:
                new_c_xy = ""
            notes.append({"name": name, "description": "", "positionxy": new_c_xy, "labelxy": ""})   
                  
        elif line.startswith("annotations"):
            new_c_xy = swap_xy(line)
            annotations.append({"name": line, "description": "", "positionxy": new_c_xy})

        elif line.startswith("annotation"):
            new_c_xy = swap_xy(line)
            number = re.findall(r'\d+', line)
            name = line[line.index(']')+1:].lstrip()
            annotations.append({"number": number[0], "name": name, "description": "", "positionxy": new_c_xy})

        elif line.startswith("market"):
            name = line[line.find(' ') + 1:line.find('[')].strip()
            new_c_xy = swap_xy(line)
            label_index = line.find("label")
            if label_index != -1:
                label = line[label_index+len("label")+1:]
            else:
                label = ""
            label = swap_xy(label)
            market.append({"name": name, "description": "", "positionxy": new_c_xy, "labelxy": label})

        elif line.startswith("style"):
            style.append(line)

        elif "->" in line:
            source, target = line.strip().split("->")
            source = source.strip()
            target = target.strip()
            links.append({"source": source, "target": target})
        else:
            continue

    return {
        "title" : title,
        "anchors" : anchors,
        "evolution" : evolution,
        "components": components,
        "links": links,
        "evolve": evolve,
        "markets": market,
        "pipelines": pipelines,
        "pioneers": pioneers,
        "notes": notes,
        "blueline": blueline,
        "style": style,
        "annotations": annotations,
        "comments": comments,
    }


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
    
    # Parse the Wardley map text
    parsed_map = parse_wardley_map(map_text)
   
    st.session_state['map_text'] = map_text
    #st.session_state['map_text'] = parsed_map
    
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
st.sidebar.write("Examples:\n\ngQuu7Kby3yYveDngy2\n\nxi4JEUqte7XRWjjhgQ\n\nMOSCNj9iXnXdbCutbl\n\nOXeRWhqHSLDXfOnrfI\n\nO42FCNodPW3UPaP8AD")
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
    st.sidebar.code(st.session_state['map_text'])

if query:
    with st.spinner("thinking... this can take a while..."):
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
