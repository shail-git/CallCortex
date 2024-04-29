from langchain_community.document_loaders.url import UnstructuredURLLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.document_compressors import LLMLinguaCompressor
from dotenv import load_dotenv
load_dotenv()

embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
compressor = LLMLinguaCompressor(model_name="lgaalves/gpt2-dolly", device_map="cpu")
stringify_docs = lambda docs: f"\n\n".join([f"Call Log {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)])

# retrive chunks for relevant text and compress prompts by removing useless tokens.  
def retrive_and_compress(query,document_list): 
    documents =  UnstructuredURLLoader(document_list).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    retriever = FAISS.from_documents(texts, embedding).as_retriever(search_kwargs={"k": 20})
    compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)
    compressed_docs = compression_retriever.invoke(query)
    return stringify_docs(compressed_docs)