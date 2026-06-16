import streamlit as st

from rag.rag_chain import get_response


# Page Config

st.set_page_config(
    page_title="NayePankh AI Assistant",
    
    layout="wide"
)

st.title(" NayePankh AI Social Impact Assistant")
st.caption(
    "Ask questions about volunteering, food drives, education programs, menstrual hygiene initiatives, and more."
)


# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []



# Sidebar

with st.sidebar:

    st.header("Options")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()


    st.subheader("💡 Suggested Questions")

    st.markdown("""
    - What is NayePankh Foundation?
    - How can volunteers organize a food distribution drive?
    - What are volunteer responsibilities?
    - How can students apply for scholarships?
    - How should menstrual hygiene awareness campaigns be conducted?
    - What should be included in an NGO impact report?
    """)

    st.divider()


    st.info(
        """
        ⚠️ Prototype Notice

        This AI assistant is a demonstration project developed for the
        NayePankh internship selection process.

        Parts of the knowledge base contain publicly available information,
        educational content, NGO best practices, and illustrative sample
        documents created for demonstration purposes.

        Responses should not be considered official organizational policies,
        procedures, or commitments unless verified by NayePankh Foundation.
        """
    )



# Memory Builder

def build_chat_history(limit=5):

    history = ""

    recent_messages = st.session_state.messages[-limit:]

    for msg in recent_messages:

        history += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    return history



# Display Previous Messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])



# Chat Input

user_query = st.chat_input(
    "Ask a question..."
)


if user_query:

    # Display User Message
    with st.chat_message("user"):
        st.markdown(user_query)

    # Store User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )

    # Build Memory
    chat_history = build_chat_history(limit=5)

    # Generate Response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer = get_response(
                user_query,
                chat_history
            )

            st.markdown(answer)

    # Store Assistant Response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )






# footer


st.divider()

st.caption(
    " Prototype AI Assistant • Built for NayePankh Foundation Internship Project • "
    "Some knowledge base content is illustrative and intended for demonstration purposes only."
)