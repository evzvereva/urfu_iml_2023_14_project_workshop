import service
from langchain import hub
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader, TextLoader
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
        url = ollama_settings.get('base_url')
        model = ollama_settings.get('model')
        
        loader = DirectoryLoader(
            path='text',
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={'autodetect_encoding': True}
        )
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
        url = ollama_settings.get('base_url')
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

        QA_CHAIN_PROMPT = hub.pull(HUB)

        qa_chain = RetrievalQA.from_chain_type(
            ollama,
            retriever=vectorstore.as_retriever(),
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )
        answer = qa_chain({"query": question})
        return answer.get('result')
