from pathlib import Path
import re

DOCUMENTS_FOLDER = "documents"


def clean_text(text):
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\n\s*\n", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def load_documents(folder_path):
    documents = []
    folder = Path(folder_path)

    for file_path in folder.glob("*.txt"):
        raw_text = file_path.read_text(encoding="utf-8")
        cleaned_text = clean_text(raw_text)

        documents.append({
            "source": file_path.name,
            "text": cleaned_text
        })

    return documents


def chunk_text(text):
    chunks = []
    paragraphs = text.split("\n")

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if paragraph != "":
            chunks.append(paragraph)

    return chunks


def create_chunks(documents):
    all_chunks = []

    for document in documents:
        chunks = chunk_text(document["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": document["source"],
                "chunk_number": i,
                "text": chunk
            })

    return all_chunks


if __name__ == "__main__":
    documents = load_documents(DOCUMENTS_FOLDER)
    chunks = create_chunks(documents)

    print(f"Loaded {len(documents)} documents")
    print(f"Created {len(chunks)} chunks")
    print()

    print("Sample chunks:")
    for chunk in chunks[:5]:
        print("--------------------")
        print(f"Source: {chunk['source']}")
        print(f"Chunk number: {chunk['chunk_number']}")
        print(chunk["text"])
        print()
