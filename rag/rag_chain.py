from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from rag.retriever import retriever

from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

prompt = ChatPromptTemplate.from_template(
    """
You are the NayePankh AI Social Impact Assistant.

Important:
The knowledge base may contain demonstration documents,
educational resources, NGO best practices, and sample content
created for a prototype system.

Do not present information as an official policy,
legal statement, or commitment of NayePankh Foundation
unless explicitly stated in the provided context.

Use the conversation history and retrieved context to answer the user's question.

Conversation History:
{chat_history}

Context:
{context}

Question:
{question}

Answer:
"""
)

def get_response(question, chat_history=""):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "chat_history": chat_history,
            "context": context,
            "question": question,
        }
    )

    return response.content