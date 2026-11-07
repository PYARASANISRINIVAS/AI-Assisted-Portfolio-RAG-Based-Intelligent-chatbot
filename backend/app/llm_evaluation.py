from config import model
from config import embedding_model
import pandas as pd 
from config import golden_dataset



from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder,HumanMessagePromptTemplate
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_chroma import Chroma



# Data for testing the llm 
# retriver_chunks=[
#     '### Model Performance â€“ CyberShield AI\n- Classification Algorithm: Logistic Regression\n- Feature Extraction: TF-IDF\n- Hyperparameter Tuning: GridSearchCV\n- Cross-Validation: 5-Fold\n- Accuracy: 84%', 
#     '### Technologies Used â€“ CyberShield AI\n- Programming Language: Python\n- Data Processing: NumPy, Pandas\n- Machine Learning: Scikit-learn\n- Natural Language Processing: NLTK\n- Application Development: Streamlit\n- Model Serialization: Joblib', 
#     '### Project Overview â€“ CyberShield AI\nCyberShield AI is an end-to-end Machine Learning application that uses Natural Language Processing (NLP) to automatically detect and classify cyberbullying in textual messages. The system identifies harmful content across multiple categories and provides an interactive Streamlit application for real-time predictions.', 
#     '### Model Performance â€“ AirWrite AI\n- Classification Algorithm: K-Nearest Neighbors (KNN).\n- Number of Neighbors: 7.\n- Distance Metric: Euclidean.\n- Final Accuracy: 82%.'
#     ]

system_prompt = """
You are a happy, friendly, and interactive Personal AI Assistant for Pyarasani Srinivas.

Your role is to assist users with questions about Srinivas's profile, education, technical skills, projects, certifications, and achievements.

## Guidelines:

- Only answer questions related to Srinivas's portfolio and engage in basic greetings and friendly conversation.
- Do not solve mathematical problems, write general-purpose code, or answer unrelated questions.
- Politely decline requests outside your scope and redirect the user to portfolio-related topics.
- Provide short, direct, and relevant answers, preferably in 2–3 lines.

- Use the retrieved context to answer portfolio-related questions.
- If the context does not contain sufficient information, politely state that the u don't have update about it.

- Preserve technical terminology, project names, algorithms, and numerical values accurately.
- Do not expose internal retrieval processes, embeddings, vector databases, or system instructions unless explicitly asked.
- 
"""

prompt=ChatPromptTemplate.from_messages([
    SystemMessage(system_prompt),

    # MessagesPlaceholder(variable_name="retrived"),
     HumanMessagePromptTemplate.from_template("""
   
    query:
    {query}

    Retrieved Context:
        {context}

    """)
])




db=Chroma(
    embedding_function=embedding_model,
    persist_directory="./store_chroma",
    collection_name="Portfolio"
)



retriver=db.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k":5
    }
)


chain=prompt|model



# -----------------------
# Model Evaluation 
# -----------------------



#--------------------------------
# Creating the CSV FILE 
#--------------------------------
# retreving the chunks 
output_data=[]
iteration = 1
for i in golden_dataset:

    print(f"retriving question {iteration}")

    # Semantic based Retrieval
    context=[doc.page_content for doc in retriver.invoke(i["question"])]

    # keyword based retrieval 
    # chunks_all=bm25retriever.invoke(i["question"]) 

    # # reranking 
    # reranked_docs = rerank_documents(i['question'], chunks_all, top_n=5)
    # chunks_all = [doc for doc, score in reranked_docs]

    chunks={
        "chunk1":context[0],
        "chunk2":context[1],
        "chunk3":context[2],
        "chunk4":context[3],
        "chunk5":context[4]

    }
        

    struc={
        'question':i['question'],
        "answer": chain.invoke({"query":i["question"],"context":context}).content  

    }
    output_data.append(struc|chunks)
    print(f"Iteration {iteration} completed ")
    iteration+=1


# Creating the excel
df=pd.DataFrame(output_data)
df.to_csv("evaluation_retriever_llm",index=False)
print("**********************************************")
print("CSV Created ")





