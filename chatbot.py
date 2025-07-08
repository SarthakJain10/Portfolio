import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
import streamlit as st

def ask_bot(input_text):

    with open("bio.txt", "r", encoding="utf-8") as file:
        doc = file.read()

    # Configuration constants
    EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
    API_TOKEN = st.secrets["api"]["hugging_face_api"]


    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " "]
    )
    # texts = text_splitter.split_text(transcript)
    texts = [t.replace("\n", " ") for t in text_splitter.split_text(doc) if t is not None]


    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    if os.path.exists("faiss_index"):
        vectorstore = FAISS.load_local("faiss_index", embeddings,  allow_dangerous_deserialization=True)
    else:
        vectorstore = FAISS.from_texts(texts, embeddings)
        vectorstore.save_local("faiss_index")

    retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={"k": 4})

    if not os.environ.get("GOOGLE_API_KEY"):
        os.environ['GOOGLE_API_KEY'] = st.secrets["api"]["google_api_key"]

    model = init_chat_model(
        "gemini-2.0-flash",
        model_provider="google-genai",
        max_output_tokens=500,
        temperature=0.3
    )

    prompt_template = """You are an AI agent named Buddy helping answer questions about Sarthak to recruiters.

    If you do not know the answer, politely admit it and let users know how to contact Sarthak to get more information.

    Use the following context to answer the question.

    Context:
    {context}

    Question:
    {question}
    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=model,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={
        "prompt": prompt,
        "document_separator": "\n\n"  # Better context separation
        }
    )

    output_response = qa_chain.invoke({"query": input_text})
    
    return output_response['result']

