from itertools import zip_longest
import streamlit as st
from streamlit_chat import message
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)

OPEN_AI_KEY = st.secrets["OPEN_AI_KEY"]

st.set_page_config(page_title="AI Mentor", page_icon=":speech_balloon:")
st.title("AI Mentor Chatbot")

# initialize session state variables
if "generated" not in st.session_state:
    st.session_state['generated'] = [] # list of generated messages

if "past" not in st.session_state:
    st.session_state['past'] = [] # stores past user inputs

if "entered_prompt" not in st.session_state:
    st.session_state['entered_prompt'] = "" # stores user input prompt


# initialize the ChatOpenAI model
chat = ChatOpenAI(
    temperature=0.5,
    model_name="gpt-3.5-turbo",
    openai_api_key=OPEN_AI_KEY,
)

def build_message_list():
    """
    Build a list of messages including system, human, and AI messages.
    """
    
    # Start zipped_messages with SystemMessage
    zipped_messages = [
        SystemMessage(content = """
            Your name is AI mentor. You are an AI Technical Expert for Artificial Intelligence, Ask User about thier name before starting and you are here to guide students with their AI-related questions.
            1. Greet the user politely, ask user name and ask how you can asist them with AI-related queries.
            2. Provide infomative and relevant responses to questions about artificail intelligence, machine learning, natural language processiing, computer vison, and related topics.
            3. You must avoid discussing senstive, offensive or harmful content. Refrain from engaging in any form of discrimination, harassment, or inappropriate behavior.
            4. If the user asks about a topic unrelated to AI, steer the conversation back to AI or politely decline to answer.
            5. Be patient and considerate. If the user is not satisfied with the response, apologize and ask for more details. Provide clear explaination.
            6. If the user expresses gratitude or indicate end of conversation, respond with a polite farewell.
            7. Do not generate long paragraphs in response. Maximum words should be 100.
            Remember, your primary goal is to assist and educate students in the field of Artifical Intelligence. Always priotize their learning experience and well-being.
            """,
        ),
    ]

    # Add together the past messages and generated messages
    for human_message, ai_message in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_message:
            zipped_messages.append(HumanMessage(content=human_message))
        if ai_message:
            zipped_messages.append(AIMessage(content=ai_message))
        return zipped_messages
    

def generate_response():
    """
    Generate AI response using the ChatOpenAI model.
    """
    # Build the list of messages
    zipped_messages = build_message_list()
    
    # Generate response using the ChatOpenAI model
    ai_response = chat(zipped_messages)
    return ai_response.content

# Define fucntion to handle user input
def submit():
    #  Set entered_prompt to the current value of the user input text box
    st.session_state['entered_prompt'] = st.session_state['user_input']
    # Clear the user input text box
    st.session_state['user_input'] = ""

# Create a text input for user
st.text_input("YOU:", key="user_input", on_change=submit)

if st.session_state['entered_prompt'] != "":
    # Get user query
    user_query = st.session_state['entered_prompt']

    # Append user query to past messages
    st.session_state['past'].append(user_query)

    # Generate response
    output = generate_response()

    # Append response to generated messages
    st.session_state['generated'].append(output)

# Display response

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        # Display AI response
        message(st.session_state["generated"][i], key=str(i))
        # Display user input
        message(st.session_state['past'][i], is_user=True, key=str(i)+"_user")