## Conversational Q&A Chatbot
import streamlit as st
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from custom_tools import search_wikipedia,get_types

## Streamlit UI
st.set_page_config(page_title="AI Pokedex")
st.header("Hey, Let's Chat about Pokemon")

# initialise open ai client
client = OpenAI()
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-0125"

# if it is a new conversation, show the conversation history as blank
if "messages" not in st.session_state:
    st.session_state.messages = []

# print messages historically with roles
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# load tools
tools = [search_wikipedia, get_types]

system_prompt = """You are a pokemon obsessed chatbot that desires to find the perfect spirit animal as a pokemon for everyone you chat to."""

# functions = [format_tool_to_openai_function(f) for f in tools]
# model = ChatOpenAI(temperature=0).bind(functions=functions)
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "{system_prompt}"),
#     ("user", "{input}"),
# ])
# chain = prompt | model | OpenAIFunctionsAgentOutputParser()

if chat_prompt := st.chat_input("Let's chat!"):
    
    st.session_state.messages.append({"role": "system", "content": system_prompt})
    st.session_state.messages.append({"role": "user", "content": chat_prompt})
    with st.chat_message("user"):
        st.markdown(chat_prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})


