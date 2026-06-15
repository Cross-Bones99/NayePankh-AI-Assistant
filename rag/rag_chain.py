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

Use the provided context and conversation history to answer the user's question.

If the answer is not present in the context, say:
"I could not find this information in the NayePankh knowledge base."

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