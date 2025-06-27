#FRONTEND CONTAINER

#pull appropriate python base image
FROM python:3.12.2 


RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    && rm -rf /var/lib/apt/lists/*


#install dependencies
RUN pip install requests streamlit

#copy the application code
COPY . .


#expose the ports for Streamlit
EXPOSE 8501

#use a script to start Streamlit
CMD ["streamlit", "run", "interface.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.fileWatcherType=none"]
