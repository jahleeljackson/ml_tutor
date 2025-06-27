#BACKEND CONTAINER

#pull appropriate python base image
FROM python:3.10


RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    && rm -rf /var/lib/apt/lists/*

#install ollama 
RUN curl -fsSL https://ollama.com/install.sh | sh

RUN ollama serve & \
    sleep 5 && \
    ollama pull mistral:latest && \
    ollama pull deepseek-r1:latest
    
#set up the Ollama environment
ENV OLLAMA_HOST="0.0.0.0"
ENV POSTGRES_URI="postgresql://postgres:9305*Elcon@localhost:5433/ml_tutor"

#install dependencies
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt 


#copy the application code
COPY . .

#expose the ports for FastAPI and Ollama
EXPOSE 8000 11434

#use a script to start both Ollama and FastAPI
COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]