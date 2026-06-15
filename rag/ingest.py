from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


DATA_DIR = "data"
VECTOR_DB_DIR = "vectorstore"


def load_markdown_files(data_dir):
    documents = []

    for file_path in Path(data_dir).rglob("*.md"):

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        documents.append(
            {
                "content": content,
                "source": str(file_path),
                "filename": file_path.name,
                "category": file_path.parent.name,
            }
        )

    return documents


def split_documents(raw_documents):

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "title"),
            ("##", "section"),
        ]
    )

    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
    )

    final_chunks = []

    for doc in raw_documents:

        md_chunks = markdown_splitter.split_text(doc["content"])

        for chunk in md_chunks:

            temp_doc = Document(
                page_content=chunk.page_content,
                metadata={
                    "source": doc["source"],
                    "filename": doc["filename"],
                    "category": doc["category"],
                    **chunk.metadata,
                },
            )

            split_chunks = recursive_splitter.split_documents([temp_doc])

            final_chunks.extend(split_chunks)

    return final_chunks


def create_vectorstore(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_DIR,
    )

    return vectorstore


def main():

    print("Loading markdown files...")

    raw_documents = load_markdown_files(DATA_DIR)

    print(f"Loaded {len(raw_documents)} documents")

    print("Splitting documents...")

    chunks = split_documents(raw_documents)

    print(f"Created {len(chunks)} chunks")

    print("Creating vector database...")

    create_vectorstore(chunks)

    print("Vector database created successfully!")

    print("\nSample Metadata:")

    if chunks:
        print(chunks[0].metadata)


if __name__ == "__main__":
    main()