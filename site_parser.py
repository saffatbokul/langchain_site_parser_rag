import requests             
from bs4 import BeautifulSoup  
import streamlit as st       
import fitz                # For reading PDF files
import io                 
# In-memory vector store for document search
from langchain_community.vectorstores import DocArrayInMemorySearch  
# Text splitter for splitting documents into smaller chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter   
# Embeddings for semantic search
from langchain_community.embeddings import HuggingFaceEmbeddings        
# For creating document objects 
from langchain.docstore.document import Document                        

# Function to find all URLs on a given webpage (excluding the base URL)
@st.cache_data
def get_page_urls(url):
    with st.spinner('Finding Urls...'):
        page = requests.get(url)                
        soup = BeautifulSoup(page.content, 'html.parser')  
        links = [link['href'] for link in soup.find_all('a') if link['href'].startswith(url) and link['href'] not in [url]] 
        links.append(url)    
        # Return a set of unique URLs                               
        return set(links)    

# Function to fetch the content (text or PDF) of a given URL
def get_url_content(url):
    response = requests.get(url)             
    # If the requested resource is a PDF file
    if url.endswith('.pdf'):                  
        pdf = io.BytesIO(response.content)  
        file = open('pdf.pdf', 'wb')         
        file.write(pdf.read())              
        doc = fitz.open('pdf.pdf')          
        # Extract and join all the text from the PDF file
        return (url, ''.join([text for page in doc for text in page.get_text()]))  
    # If the requested resource is an HTML file or any other text format
    else:                                   
        soup = BeautifulSoup(response.content, 'html.parser')  
        text = soup.get_text()              
        lines = (line.strip() for line in text.splitlines())  
        # Split the text into smaller chunks
        chunks = (phrase.strip() for line in lines for phrase in line.split('  '))  
        # Join the non-empty chunks with newline characters
        text = '\n'.join(chunk for chunk in chunks if chunk)
         # Return a tuple containing the URL and the extracted text  
        return (url, text)                                  

# Function to create an in-memory document search index using the Langchain library
@st.cache_resource
def get_retriever(urls):
    with st.spinner('Finding Urls...'):
        # Fetch the content of each URL
        all_content = [get_url_content(url) for url in urls]  
        # Create a list of Document objects using the fetched content
        documents = [Document(page_content=doc, metadata={'url': url}) for (url, doc) in all_content]  
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
        # Split the documents into smaller chunks
        docs = text_splitter.split_documents(documents)    
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        # Create an in-memory vector store using the split documents and their embeddings  
        db = DocArrayInMemorySearch.from_documents(docs, embeddings)  
         # Create a document retriever using Maximal Marginal Relevance (MMR) algorithm
        retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 5, "fetch_k": 10}) 
        # Return the document retriever object
        return retriever                      
