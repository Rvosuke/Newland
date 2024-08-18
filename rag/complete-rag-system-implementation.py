import os
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.retrievers import ParentDocumentRetriever, BM25Retriever, EnsembleRetriever
from langchain.storage import InMemoryStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain.llms.base import LLM
from typing import Any, List, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from operator import itemgetter
import pandas as pd

# Load PDF documents
def load_pdf_documents(pdf_folder_path: str) -> list:
    base_docs = []
    
    if not os.path.exists(pdf_folder_path):
        raise FileNotFoundError(f"The folder '{pdf_folder_path}' does not exist.")

    for file in os.listdir(pdf_folder_path):
        if file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder_path, file)
            print(f"Processing: {pdf_path}")
            try:
                loader = PyPDFLoader(pdf_path)
                pages = loader.load()
                base_docs.extend(pages)
            except Exception as e:
                print(f"Error processing {pdf_path}: {str(e)}")

    return base_docs

# Custom LLM class for ChatGLM3
class ChatGLM3_LLM(LLM):
    tokenizer: AutoTokenizer = None
    model: AutoModelForCausalLM = None

    def __init__(self, model_path: str):
        super().__init__()
        print("Loading model from local...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True).half().cuda()
        self.model = self.model.eval()
        print("Local model loading completed")

    def _call(self, prompt: str, stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              **kwargs: Any):
        response, history = self.model.chat(self.tokenizer, prompt, history=[])
        return response
        
    @property
    def _llm_type(self) -> str:
        return "ChatGLM3-6B"

# Initialize models and embeddings
pdf_folder_path = '3DGS'
base_docs = load_pdf_documents(pdf_folder_path)

model_path = os.path.expandvars("$GEMINI_PRETRAIN2/chatglm3-6b")
primary_qa_llm = ChatGLM3_LLM(model_path)

EMBEDDING_PATH = os.path.expandvars('$GEMINI_PRETRAIN/bge-m3')
embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_PATH)

# Define text splitters
base_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1500)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=200)

# 1. Base Retriever
base_docs_split = base_splitter.split_documents(base_docs)
base_vectorstore = Chroma.from_documents(base_docs_split, embeddings)
base_retriever = base_vectorstore.as_retriever(search_kwargs={"k": 2})

# 2. Parent Document Retriever (PDR)
vectorstore = Chroma(collection_name="split_parents", embedding_function=embeddings)
store = InMemoryStore()
pdr = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)
pdr.add_documents(base_docs)

# 3. Ensemble Retriever (ER)
bm25_retriever = BM25Retriever.from_documents(base_docs_split)
bm25_retriever.k = 3
chroma_retriever = base_vectorstore.as_retriever(search_kwargs={"k": 3})
er = EnsembleRetriever(
    retrievers=[bm25_retriever, chroma_retriever],
    weights=[0.75, 0.25]
)

# Create QA chains
template = """Please answer the following question based on the provided context information. If you think the question cannot be answered based on the provided information, please answer 'I don't know':

### Context Information
{context}

### Question
Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

def create_qa_chain(retriever):
    return (
        {"context": itemgetter("question") | retriever,
         "question": itemgetter("question")
        }
        | RunnablePassthrough.assign(
            context=itemgetter("context")
          )
        | {
             "response": prompt | primary_qa_llm,
             "context": itemgetter("context"),
          }
    )

base_qa = create_qa_chain(base_retriever)
pdr_qa = create_qa_chain(pdr)
er_qa = create_qa_chain(er)

# Prepare questions and ground truth answers
questions_and_answers = [
    {
        "question": "What is 3D Gaussian Splatting?",
        "ground_truth": "3D Gaussian Splatting is an emerging technique for 3D scene representation and rendering. It uses 3D Gaussian functions to represent points in a scene, each with its own position, scale, orientation, and color attributes. This method efficiently represents and renders complex 3D scenes, particularly excelling in handling scenes reconstructed from multi-view images."
    },
    # ... (include all other questions and ground truths here)
]

# Execute queries and save results
results = []
for idx, qa in enumerate(questions_and_answers, 1):
    question = qa["question"]
    ground_truth = qa["ground_truth"]
    
    base_result = base_qa.invoke({"question": question})
    pdr_result = pdr_qa.invoke({"question": question})
    er_result = er_qa.invoke({"question": question})
    
    results.append({
        "index": idx,
        "question": question,
        "ground_truth_answer": ground_truth,
        "base_retriever_chunks_size1000_overlap100_k2": str(base_result["context"]),
        "base_retriever_answer_size1000_overlap100_k2": base_result["response"],
        "PDR_chunks_psize1500_csize200": str(pdr_result["context"]),
        "PDR_answer_psize1500_csize200": pdr_result["response"],
        "ER_chunks_size1000_overlap100_k3_w75": str(er_result["context"]),
        "ER_answer_size1000_overlap100_k3_w75": er_result["response"],
    })

# Save results to CSV
df = pd.DataFrame(results)
df.to_csv("rag-result.csv", index=False)
