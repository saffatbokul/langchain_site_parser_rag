
# Chat with a website using Langchain + Streamlit + Llama.cpp + Docker

This project will crawl a website given the URL, save the content (HTML and PDF) to the memory and then. will allow users to chat with the website content using the power of large language models (Microsoft Phi-2). To get started you can either use my pre built **docker container** (easiest) or run it manually.

## Using Docker

The container is available at the [docker hub](https://hub.docker.com/layers/saffatbokul/langchain_site_parser_rag/latest/images/sha256-693cd1e7a3a816e08a4f5a54a5236d2ad1dc849145334ac67194a7fc98477fff?context=explore).

You need docker [installed](https://docs.docker.com/engine/install/ubuntu/) on your system.

After installing docker, run the following command to pull the image.

```
docker pull saffatbokul/langchain_site_parser_rag:latest
```
Now, run the image
```
docker run -p 8501:8501 langchain_site_parser_rag
```
You can also build you own image with the dockerfile provided in this repo.

## Running Manually

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
Run the app.
```
streamlit run main.py --server.port 8501
```
Now open localhost:8501 and play with it !