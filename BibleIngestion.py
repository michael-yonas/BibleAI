from typing import Any,Dict,List

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_huggingface import HuggingFaceEmbeddings
from logger import (Colors, log_error, log_header, log_info, log_success, log_warning)
from dotenv import load_dotenv

load_dotenv()

def read_contents(filename: str) -> List[Document]:
    verses = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue  # Skip blank lines
                if "\t" in line:
                    reference, verse_text = line.split("\t", 1)
                else:
                    parts = line.split(" ", 1)
                    reference = parts[0]
                    verse_text = parts[1] if len(parts) > 1 else ""

                verses.append(
                    Document(
                        page_content=verse_text,
                        metadata={
                            "reference": reference,
                            "source": filename
                        }
                    )
                )
        return verses
    except Exception as e:
        log_error(f"Error loading {filename}: {e}")
        return []

def load_contents(verses :List[str],postgresdb):
    try:
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        CONNECTION_STRING = "postgresql+psycopg2://GenAI:yourpassword@localhost:5432/postgres"

        vectorstore = PGVector.from_documents(
            documents=verses,
            embedding=embedding_model,
            connection="postgresql+psycopg2://GenAI:Messi2012$@localhost:5433/postgres",
            collection_name="bible_collection",
            pre_delete_collection=False  # <-- This prevents dropping/recreating the collection
        )

        #vectorstore.add_documents(verses)
        return 0
    except Exception as e:
        log_error(f"Error loading in embeddings: {e}")
        return -1
postgres=os.environ["POSTGRESDETAILS"]
verses=read_contents(r"data\kjv_Bible.txt",postgres)
result = load_contents(verses)

print(result)
