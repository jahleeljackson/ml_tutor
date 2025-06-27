# Machine Learning Tutor 
<img width="500" alt="Screenshot 2025-06-27 at 11 24 57 AM" src="https://github.com/user-attachments/assets/79769ec4-a191-4a21-a131-f5489f00ceff" />
<img width="500" alt="Screenshot 2025-06-27 at 11 37 38 AM" src="https://github.com/user-attachments/assets/87535472-9ff5-480d-b764-7f8743093658" />


## Description 

### What is it?
A chatbot with expertise in the domain of machine learning and general software topics. 
### What does it do?
The chatbot utilizes a LLM integrated with **retrieval-augmented generation (RAG)** to provide relevant context specific to the domain of machine learning concepts. 
Additionally, the most current information and data is scraped from reputable sources such as [The Gradient](https://thegradient.pub/) and [Distill](https://distill.pub/). 
This data is scraped, processed, and embedded into a [FAISS](https://faiss.ai/index.html) vector database on an **automated schedule**. Users have access to two Ollama models: Mistral and DeepSeek-R1.

Preloaded as context in the FAISS vector database are the following texts:
1. *Designing Data-Intensive Applications* by Martin Kleppman
2. *Designing Machine Learning Systems* by Chip Huyen
3. *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* by Aurélien Géron
4. *Introduction to Machine Learning with Python* by Andreas C. Muller and Sarah Guido
5. *Machine Learning Engineering* by Andriy Burkov
6. *Pattern Recognition and Machine Learning* by Christopher M. Bishop
7. The Pandas Documentation
8. The Python Documentation
9. The Scikit-learn Documentation
10. The SQL Manual

### Motivations 
As with every project, I aimed to accomplish two objectives: 
1. **Learn something new**
2. **Solve a problem**

#### The Problem 
I interface with LLM's on a daily basis (mostly DeepSeek and ChatGPT) but found that sometimes information generated was irrelevant, outdated, or that my prompt was misinterpreted (specifically ML related questions).
I longed for an LLM interface that didn't require that I provide specific context in order to get relevant and up to date information. So, the key features to be implemented were:
- RAG for accurate context
- Prompt templates for prompt context
- Automated knowledge updates for relevant and up to date information

#### What I Learned
What didn't I learn with this project. Though this was not my first Python project, this is the first in which I used Docker, the Google Cloud Platform, LangChain, Postgres, FastAPI, APScheduler, and python's virtual environments.

### Technology Stack 
- LangChain
- HuggingFace
- FastAPI
- Docker
- Google Cloud Platform
- APScheduler
- Streamlit
- PostgreSQL / Psycopg2
- FAISS
- Requests
- BeautifulSoup
  
### Challenges & Features to Implement 
Every new technology presented a challenge, but a few of the standouts were:
- Docker (was easy once it clicked)
- PostgreSQL integration with FastAPI
- Development of the chatbot and vectorDB classes
- Reliable scraping of thegradient and distill.pub
  
## Instructions to Run 

1. Clone this repository.
2. Ensure that you have docker installed on your machine
3. Navigate to the app/ directory in terminal.
4. Run the following command:
```bash
docker build -t ml-tutor-app .
```
5. Once the operation is complete, run the following:
 ```bash
docker-compose up
 ```
6. Navigate to [http://127.0.0.1:8501/](http://127.0.0.1:8501/)


## Resources 
- [Streamlit Documentation](https://docs.streamlit.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostreSQL Documentation](https://www.postgresql.org/docs/)
- [Psycopg2 Documentation](https://www.psycopg.org/docs/)
- [LangChain Documenation](https://python.langchain.com/docs/introduction/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [APScheduler Documentation](https://apscheduler.readthedocs.io/en/3.x/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://requests.readthedocs.io/en/latest/)
  
