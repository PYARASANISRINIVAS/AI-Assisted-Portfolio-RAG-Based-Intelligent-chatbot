from app.rag_chatbot import chat_with_model

while True:
    query =input()
    if query=="break":
        break
    else:
        chat_with_model(query)