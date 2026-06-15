from rag.rag_chain import get_response

while True:

    question = input("\nQuestion: ")

    if question.lower() == "exit":
        break

    answer = get_response(question)

    print("\nAnswer:")
    print(answer)