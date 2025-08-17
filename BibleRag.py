from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.chat_models import ChatOllama

load_dotenv()

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_postgres import PGVector

from langchain_huggingface import HuggingFaceEmbeddings


def run_llm(query : str):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    docsearch = PGVector.from_existing_index(
        collection_name="langchain_pg_embedding",
        connection="postgresql+psycopg2://GenAI:Messi2012$@localhost:5433/postgres",
        embedding=embeddings
    )

    chat = ChatOllama(verbose=True,temperature=0)

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    stuff_documents_chain = create_stuff_documents_chain(chat,retrieval_qa_chat_prompt)
    qa = create_retrieval_chain(
        retriever=docsearch.as_retriever(),combine_docs_chain=stuff_documents_chain
    )
    result = qa.invoke(input={"input": query})
    new_result = {
        "query" : result["input"],
        "result" : result["answer"],
        "source_documents" : result["context"],
    }

    return new_result

'''
if __name__ == "__main__":
    res = run_llm(query="Summary about Genesis")
    print(res)
'''
