
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import FAISS
import time

from models import embedding_model
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

documents=splitter.split_text(data)


# # Faiss DB Creation 
# db=FAISS.from_documents(
#     documents=chunks,
#     embedding=embedding_model
# )


# db.save_local(r"FAISS","faiss_index")


# Chroma DB Creation 

from langchain_chroma import Chroma


chroma_db=Chroma(
    embedding_function=embedding_model,
    collection_name="Portfolio",
    persist_directory="./store_chroma"

)


# Process documents batch by batch
batch_size = 10
total_documents = len(documents)

for i in range(0, total_documents, batch_size):

    batch = documents[i:i + batch_size]

    chroma_db.add_documents(batch)

    processed = min(i + batch_size, total_documents)

    print(f"Processed {processed}/{total_documents} documents")

    # Wait before processing the next batch
    if processed < total_documents:
        print("Waiting 5 seconds...")
        time.sleep(5)

print("All document embeddings stored successfully!")







