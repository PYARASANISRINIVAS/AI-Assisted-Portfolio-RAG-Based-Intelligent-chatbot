
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import FAISS

from model_defination import embedding_model
# loading the markdown file

with open(r"..\knowledge_base\Personal_Knowledge_Base.md","r") as f:
    data=f.read()


# splitting the text file 

splitter=MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#","level 1"),
                         ("##","level 2"),
                         ("###","level 3")
                         ],
                         strip_headers=False,
                         )

chunks=splitter.split_text(data)


# Faiss DB Creation 
db=FAISS.from_documents(
    documents=chunks,
    embedding=embedding_model
)


db.save_local(r"FAISS","faiss_index")


# Chroma DB Creation 

from langchain_chroma import Chroma
from vector_embeddings import chunks
chroma_db=Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    collection_name="Portfolio",
    persist_directory="./store_chroma"

)







