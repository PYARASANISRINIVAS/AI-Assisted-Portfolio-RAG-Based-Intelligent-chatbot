# imports 

# from dotenv import  load_dotenv
# from langchain_groq import ChatGroq
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings


# load_dotenv()


# # Creating the chat model 
# chat_model=ChatGroq(
#     model='openai/gpt-oss-120b',
#     temperature=0,
#     max_tokens=500,
# )
# print("Chat model created  Succesfully !  " )


# # Creating the embedding model 
# embedding_model=HuggingFaceEmbeddings(model="sentence-transformers/all-mpnet-base-v2")
# print("embedding  model created  Succesfully !  " )

import os 
print("Starting models.py...", flush=True)

from dotenv import load_dotenv
from langchain_groq import ChatGroq
# from langchain_huggingface import HuggingFaceEndpointEmbeddings


load_dotenv()

print("Initializing Groq model...", flush=True)

chat_model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    max_tokens=500,
)

print("Groq model initialized!", flush=True)

print("Loading Hugging Face embedding model...", flush=True)

# embedding_model = HuggingFaceEmbeddings(
#     model="sentence-transformers/all-mpnet-base-v2"
# )


# embedding_model = HuggingFaceEndpointEmbeddings(
#     model="sentence-transformers/all-mpnet-base-v2",
#     task="feature-extraction",
#     huggingfacehub_api_token=os.getenv("HF_TOKEN")
# )


embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2",
    output_dimensionality=768,  # Suggested: 768, 1536, or 3072 (default)
)



# embedding_model = HuggingFaceEmbeddings(
#     model="sentence-transformers/paraphrase-albert-small-v2"
# )



print("Embedding model loaded successfully!", flush=True)
