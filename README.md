# rag-app

This app enables question answering using the Retrieval-Augmented Generation (RAG) technique. It combines a document retrieval system with a language model to generate accurate and context-aware responses.

## Requirmnets 

- python 3.10 or later

### Install python using MiniConda

1) Download and install miniconda from [here](https://www.anaconda.com/docs/getting-started/miniconda/install#linux)

2) Create a new environment using the following command :
``` bash 
$ conda create -p .venv python=3.10
```

3) Activate the environment 
```bash 
$ conda activate .venv/ 
```

4) (Optional) setup your command line for better readiability 

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$"
```

## Installation 

### Intall the require packages 

```bash
$ pip install -r requirements.txt
```

### Setup the environmnet variables
```bash
$ cp .env.example .env
```

Set your environment variables in the 'env' file. Like "OPENAI_API_KEY" value.

## Run Docker Compose Services 
```bash
$ cd docker
$ cp .env.example .env 
```

- update `.env` with your credential

## RUN FastAPI  server 
```bash 
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
