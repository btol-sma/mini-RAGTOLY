# Toly-Rag: A Minimal Implementation of RAG Model
This project is a minimal implementation of the RAG (Retriever-augmented generation) . It is based on the tutorial for creating a RAG model from scratch [mini-RAG | From notebooks to the PRODUCTION](https://youtube.com/playlist?list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj&si=up6PyBEHtkLrrfHb) , and it's been structured using Clean Architecture for better maintainability, scalability, and separation of concerns.

## Requirements

- Python 3.8 or later
- Install Python using MiniConda

### Install MiniConda
Download and install MiniConda from [here](https://docs.conda.io/en/latest/miniconda.html).

### Create a new environment
To create the environment, run the following command:

```bash
$ conda create -n mini-rag python=3.8

### Activate the environment
```bash
$ conda activate mini-rag

## Installation
1. Install the required packages  
```bash 
$ pip install -r requirements.txt

2. Setup the environment variables 
```bash 
$ cp .env.example .env

3. Run the FastAPI server
```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000

## FastAPI Setup
- The server will run on http://127.0.0.1:5000.
- You can access the interactive API documentation at http://127.0.0.1:5000/docs.


