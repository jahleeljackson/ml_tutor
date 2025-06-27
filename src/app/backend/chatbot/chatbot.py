from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from .vectorstore import VectorStore

class Chatbot():

    def __init__(self, model="mistral"):
        
        self.model= model
       
        if self.model == "deepseek-r1":
            llm = OllamaLLM(
            model="deepseek-r1",
            temperature=0.1,
            )
        else:
            llm = OllamaLLM(
                model=self.model, # "mistral"
                temperature=0.1,
            )
        
        template = """
        You are a machine learning tutor who has decades of experience in the fields of 
        machine learning / artificial intelligence,
        programming,
        data science,
        software,
        technology,
        system design,
        and MLOps.

        You are excellent at generating code,
        answering questions,
        breaking down complex concepts,
        providing other sources for additional learning (especially if you don't know or are not sure about the answer),
        as well as providing detailed explanations when prompted to.

        Context: {context}
        Question: {question}
        Answer: 
        """

        prompt = PromptTemplate(
            template=template, 
            input_variables=["context", "question"]
        )

        vectorstore = VectorStore()
        
        self.ragchain = (
            {"context": vectorstore.vectorstore.as_retriever(), "question" : RunnablePassthrough()}
            | prompt 
            | llm 
            | StrOutputParser()
            )
        
        


    def invoke(self, input: str):
        return self.ragchain.invoke(input)