
# Chat with a website using Langchain + Streamlit + Llama.cpp + Docker

This is a very simple project that will crawl a website given the URL, save the content (HTML and PDF) to the memory and then. will allow users to chat with the website content. To get started do the following:

Clone the repo:

```
git clone https://github.com/saffatbokul/langchain_site_parser_rag.git
```
Create a ./models directory:
```
cd langchain_site_parser_rag
mkdir models
```
Go into the models directory and download the phi-2 model from Huggingface:
```
cd models
wget https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf?download=true -O phi-2.Q4_K_M.gguf
```
Go back to root directory, and create a virtual env (not shown). Then install the required libraries.

```
cd ../
pip install -r requirements.txt
```
Check if the server is working locally
```
streamlit run main.py --server.port 8080
```
If you want to dockerize this app, you need to install docker first on your system. Here is a command line installation guide for ubuntu -> https://docs.docker.com/engine/install/ubuntu/.

