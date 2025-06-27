import requests
import streamlit as st 
import os


PROMPT_POST_URL = "http://backend:8000/generate-response"
DEEPSEEK_PROMPT_POST_URL = "http://backend:8000/generate-complex-response"
CONTEXT_URL = "http://backend:8000/context"
MODEL = "mistral"

st.set_page_config(page_title="Machine Learning Tutor")

with st.sidebar:
    st.title("Machine Learning Tutor")
    st.markdown("Welcome to the Machine Learning Tutor! Ask any questions related to machine learning, data science, or programming, and get (not so) instant answers.")
    
    st.markdown("### Model Selection")
    model = st.selectbox(
        "Select a model:",
        ["mistral", "deepseek-r1"],
        index=0
    )
    
    if model == "deepseek-r1":
        PROMPT_POST_URL = DEEPSEEK_PROMPT_POST_URL
        MODEL = "deepseek-r1"
    

    st.markdown("#### Tips:")
    st.markdown("**The DeepSeek-R1 model is more powerful and can handle complex queries better, but it may take longer to respond.**")
    st.markdown("**Use Mistral for more casual questions or when you need quicker responses.**")
# function for generating LLM response
def generate_response(input): 
    data = {
        "prompt": input,
    }
    response = requests.post(PROMPT_POST_URL, json=data)     
    
    if response.status_code != 200:
        st.error("Error generating response. Please try again later.")
        return "Error generating response."
    
    response = response.json()
    return response["response"]

# function for posting context to the backend
def post_context(response, model="mistral", role="user"):
    data = {
        "context_text": response,
        "model": model,
        "role": role
    }
    response = requests.post(CONTEXT_URL, json=data)
    if response.status_code != 200:
        st.error("Error posting context. Please try again later.")
        return "Error posting context."
    
    return response.json()    

def get_context():
    response = requests.get(CONTEXT_URL)
    if response.status_code != 200:
        st.error("Error retrieving context. Please try again later.")
        return []
    context = []
    for item in response.json():
        context.append(item["context_text"])
    return context


# welcome message if no chats have occurred
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "Machine Learning Tutor", "content": "Welcome to the Machine Learning Tutor!"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User-provided prompt
if input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": input})
    with st.chat_message("user"):
        st.write(input)

# Generate a new response if last message is not from tutor
if st.session_state.messages[-1]["role"] != "Machine Learning Tutor":
    with st.chat_message("Machine Learning Tutor"):
        with st.spinner("Generating an answer for you..."):
            #context = get_context()
            response = generate_response(input) 
            st.write(response) 
            post_context(response, model=MODEL, role="model")
    message = {"role": "Machine Learning Tutor", "content": response}
    st.session_state.messages.append(message)
