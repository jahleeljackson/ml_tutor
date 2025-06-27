from langchain_community.document_loaders import TextLoader
from langchain.schema import Document 
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_community.vectorstores import FAISS

class VectorStore():
    def __init__(self, file_path: str = "chatbot/vectorstore_dir/"):
        self.file_path = file_path
        try:
            vectorstore = FAISS.load_local(
                file_path,
                embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
                allow_dangerous_deserialization=True
            )
            print(f"Vector store loaded from {file_path}.")
            self.vectorstore = vectorstore
            print("Vector store loaded successfully.")
        except Exception as e:
            print(f"Could not load vector store from file path, creating new one now: {e}")
             #load initial texts to be embedded for RAG
            file_paths = [
                'src/initial_rag_content/designing_data_intensive_applications.txt',
                'src/initial_rag_content/designing_ml_systems.txt',
                'src/initial_rag_content/hands_on_ml.txt',
                'src/initial_rag_content/intro_to_ml.txt',
                'src/initial_rag_content/machine_learning_engineering.txt',
                'src/initial_rag_content/pattern_recognition_and_machine_learning.txt',
                'src/initial_rag_content/pandas_documenation.txt',
                'src/initial_rag_content/python_documentation.txt',
                'src/initial_rag_content/python_tutorial.txt',
                'src/initial_rag_content/scikit_learn_documentation.txt',
                'src/initial_rag_content/sql_manual.txt'
            ]

            documents = []
            for file_path in file_paths:
                try:
                    documents.extend(TextLoader(file_path=file_path).load())
                    print(f"Loaded file: {file_path}")
                except Exception as e:
                    print(f"Error loading file {file_path}: {e}")

            #defining text_splitter to split the documents into manageable chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=300,
                add_start_index=True,
            ) 
            
            #retrieving chunks of text
            try:
                chunks = text_splitter.split_documents(documents)
                if not chunks:
                    raise ValueError("No chunks were created from the documents.")
                else:
                    print(f"Split documents into {len(chunks)} chunks.")
            except Exception as e:
                print(f"Error splitting documents: {e}")

            #setting up embedding function using HuggingFace embeddings
            embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            print("Embedding function created using HuggingFace embeddings.")
            #creating vector store of domain specific embeddings
            self.vectorstore= FAISS.from_documents(chunks, embedding_function)

        
        
    def update_vectorstore(self, chunks: list[Document]):
        """Updates the vector store with new documents."""
        try:
            self.vectorstore.add_documents(chunks)
            print("Vector store updated with new documents.")
        except Exception as e:
            print(f"Error updating vector store: {e}")

    def save_vectorstore(self, file_path : str = "src/app/chatbot/vectorstore_dir"):
        """Saves the vector store to a file."""
        try:
            self.vectorstore.save_local(file_path)
            print(f"Vector store saved to {file_path}.")
        except Exception as e:
            print(f"Error saving vector store: {e}")



if __name__ == '__main__':
    print("Initializing vector store...")
    vectorstore = VectorStore()
    print("Vector store initialized. Adding initial documents...")
    # Save the vector store to a file
    vectorstore.save_vectorstore()
    print("Initial documents added and vector store saved.")
    print("Vector store initialized and saved successfully.")