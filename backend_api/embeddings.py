import service
from langchain import hub
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings import OllamaEmbeddings
from langchain.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

logger = service.getLogger(__name__)

VECTORESTORE_DIRECTORY = '.chromadb'
HUB = 'rlm/rag-prompt-llama'

def create_vectorestore():
    settings = service.load_settings()
    ollama_settings = settings.get('ollama')
    if ollama_settings is not None:
        url = ollama_settings.get('url')
        model = ollama_settings.get('model')

        loader = TextLoader('text')
        data = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        all_splits = text_splitter.split_documents(data)

        oembed = OllamaEmbeddings(base_url=url, model=model)
        Chroma.from_documents(
            documents=all_splits,
            embedding=oembed,
            persist_directory=VECTORESTORE_DIRECTORY
        )

def chain_prompt(question: str) -> str:
    settings = service.load_settings()
    ollama_settings = settings.get('ollama')
    if ollama_settings is not None:
        url = ollama_settings.get('url')
        model = ollama_settings.get('model')

        ollama = Ollama(
            base_url=url,
            model=model,
            temperature=0.1,
            verbose=True
        )

        oembed = OllamaEmbeddings(base_url=url, model=model)
        vectorstore = Chroma(
            embedding_function=oembed,
            persist_directory=VECTORESTORE_DIRECTORY
        )

        docs = vectorstore.similarity_search(question)
        print(len(docs))

        QA_CHAIN_PROMPT = hub.pull(HUB)

        qa_chain = RetrievalQA.from_chain_type(
            ollama,
            retriever=vectorstore.as_retriever(),
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )
        return qa_chain({"query": question}).result
