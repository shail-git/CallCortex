from langchain_community.document_loaders.url import UnstructuredURLLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.document_compressors import LLMLinguaCompressor


def compress_docs(query,document_list): 
    documents =  UnstructuredURLLoader(document_list).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
    retriever = FAISS.from_documents(texts, embedding).as_retriever(search_kwargs={"k": 20})

    compressor = LLMLinguaCompressor(model_name="openai-community/gpt2", device_map="cpu")
    compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)
    compressed_docs = compression_retriever.invoke(query)
    stringify_docs = lambda docs: f"\n\n".join([f"Call Log {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)])
    return stringify_docs(compressed_docs)