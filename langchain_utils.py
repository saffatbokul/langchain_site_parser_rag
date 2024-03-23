# Import required modules
from langchain_community.llms import LlamaCpp
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import streamlit as st

# Define a function to create a conversational retrieval chain with the given retriever
@st.cache_resource
def langchain_create(_retriever):
    # Initialize the LlamaCpp language model
    llm = LlamaCpp(
        model_path="models/phi-2.Q4_K_M.gguf",  # Path to the model file
        temperature=0.5,                      # Controls precision of predictions
        n_ctx=2048,                            # Maximum context length for the model
        top_p=1,                              # Parameter for nucleus sampling (higher values result in more deterministic outputs)           
    )
    
    # Initialize conversation memory buffer
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Create a conversational retrieval chain using the initialized language model and retriever
    created_chain = ConversationalRetrievalChain.from_llm(
        llm, retriever=_retriever, memory=memory, verbose=False
    )
    
    # Return the created conversational retrieval chain
    return created_chain
