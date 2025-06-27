#!/bin/bash

# Start Ollama in the background
ollama serve &

# Wait a few seconds to ensure Ollama is ready
echo "Starting Ollama..."
sleep 5



# Start FastAPI
echo "Starting FastAPI..."
uvicorn main:app --host 0.0.0.0 --port 8000