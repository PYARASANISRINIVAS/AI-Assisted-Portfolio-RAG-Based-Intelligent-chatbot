# imports 

from dotenv import  load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings



load_dotenv()


# Creating the chat model 
chat_model=ChatGroq(
    model='openai/gpt-oss-120b',
    temperature=0,
    max_tokens=500,
)
print("Chat model created  Succesfully !  " )


# Creating the embedding model 
embedding_model=HuggingFaceEmbeddings(model="sentence-transformers/all-mpnet-base-v2")
print("embedding  model created  Succesfully !  " )


