from rag.retriever import retriever

query = "What are volunteer responsibilities?"

docs = retriever.invoke(query)

for i, doc in enumerate(docs, 1):
    print(f"\nChunk {i}")
    print("=" * 50)
    print(doc.page_content)
    print("\nMetadata:", doc.metadata)