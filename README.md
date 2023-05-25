# Have an AI Chat with your Wardley Map
Chat with your Wardley Map. Enter the map id and the map will be downloaded from OnlineWardleyMaps.com.

## Setup
Clone this repository and use Streamlit to point to this repository.

## How to Use
- On the sidebar, enter the ID of the Wardley Map that you want to chat about.
- Enter your question in the input field labeled "Question: ".
- Press enter or click outside the input box to submit your question. The application will use GPT-4 to generate a response.
- You can ask as many questions as you like. The history of your questions and the corresponding answers will be kept in the main panel.

## Features
- Allows users to input a Wardley Map ID
- Downloads the map data from the Wardley Map API
- Uses GPT-4 to generate and answer questions about the Wardley Map
- Retains past questions and answers for user reference

## How to Run
1. Clone the repository.
2. Set the OpenAI API key in the Streamlit secrets manager.
3. Run the streamlit app using the command streamlit run main.py.

## Dependencies
To run this code, you need the following Python packages:

- streamlit
- streamlit-chat
- streamlit-option-menu
- openai

### API Keys
The application uses the OpenAI API. You will need to obtain an API key from OpenAI and set it in the Streamlit secrets manager.

## Developer Info
This application is developed by Mark Craddock. You can follow him on Twitter at https://twitter.com/mcraddock.

## Version Info
The current version of this application is 0.1.4.

## Disclaimer
This application is not optimized and may run out of OpenAI credits. Also, Wardley Mapping is provided courtesy of Simon Wardley and is licensed under Creative Commons Attribution Share-Alike.

Please use responsibly and in accordance with OpenAI's use-case policy.

## License
This project is licensed under Creative Commons Attribution Share-Alike.
