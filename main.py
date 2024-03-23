import streamlit as st
from site_parser import *
from langchain_utils import *
st.set_page_config(
    page_title="Chat with a website using Langchain + Streamlit + Llama.cpp + Docker"
)

with st.sidebar:

    st.subheader('Chat with any website!', divider='rainbow')
    st.markdown('Built with: **Streamlit** for frontend, **Langchain** for RAG functionality, **Llama.cpp** for loading the GGUF model, and **Docker** for deployment.')
    st.markdown('By default we are using a Q_4_k_M version of the _Phi-2_ model with 2.7 billion parameters from Microsoft.')
    st.markdown('This tool has been deployed on a server with a single ARM core (No GPU :( ), so please be patient with the text generation :)')
    st.markdown('View the source code on [Github](https://duckduckgo.com)')


if "website_url" not in st.session_state:
    st.session_state.website_url = ""

website_url = st.text_input("Which URL would you like to chat with?", key="website_url")
system_prompt = "You are an expert text summarizer. You will be given a block of text and asked to summarize it."

if st.session_state.website_url != "":
    urls = get_page_urls(website_url)
    retriever = get_retriever(urls)
    if "messages" not in st.session_state:

        st.session_state.messages = [
            {"role": "assistant", "content": "I have stored the contents of the website in memory ! What would you like to know?"}
        ]

    if "current_response" not in st.session_state:
        st.session_state.current_response = ""

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    llm_chain = langchain_create(retriever)
    if user_prompt := st.chat_input("Your message here", key="user_input"):
        st.session_state.messages.append(
            {"role": "user", "content": user_prompt}
        )
        with st.chat_message("user"):
            st.markdown(user_prompt)
        with st.spinner('Generating a response, might take a while...'):
            response = llm_chain.run(user_prompt)
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
        with st.chat_message("assistant"):
            st.markdown(response)