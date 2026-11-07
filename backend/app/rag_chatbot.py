from app.models import chat_model
from app.models import embedding_model
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

history=[]
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
    persist_directory="./app/store_chroma",
    collection_name="Portfolio"
)



retriver=db.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k":5
    }
)


chain=prompt|chat_model


def chat_with_model(query:str):
    context=[doc.page_content for doc in retriver.invoke(query)]
    print(context)
    answer=chain.invoke({"query":query,"context":context,"history":history}).content
    print(answer)
    return answer
        








