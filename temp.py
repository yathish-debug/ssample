import streamlit as st
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import os

# Set environment variables
os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "fa61d3bcde7c8965f6b10c1b4995276bb452a0a75bdd96327046d2829b60bf5e"

@st.cache(allow_output_mutation=True)
def process_pdf(pdf_path):
    try:
        # Read PDF
        pdfreader = PdfReader(pdf_path)
        raw_text = ''
        for page in pdfreader.pages:
            content = page.extract_text()
            if content:
                raw_text += content

        # Split text
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=800,
            chunk_overlap=200,
            length_function=len,
        )
        texts = text_splitter.split_text(raw_text)

        # Download embeddings from OpenAI
        embeddings = OpenAIEmbeddings()

        # Create document search
        document_search = FAISS.from_texts(texts, embeddings)

        return document_search
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return None

def main():
    st.title("PDF Question Answering App")

    # Upload PDF file
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:
        document_search = process_pdf(uploaded_file)

        if document_search:
            # Get user query
            query = st.text_input("Enter your question:")
            if st.button("Get Answer"):
                try:
                    # Load question answering chain
                    chain = load_qa_chain(OpenAI(), chain_type="stuff")
                    # Perform question answering
                    docs = document_search.similarity_search(query)
                    answer = chain.run(input_documents=docs, question=query)
                    # Display answer
                    st.write("Answer:", answer)
                except Exception as e:
                    st.error(f"Error processing question: {e}")

if __name__ == "__main__":
    main()
