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
TEXT_DIRECTORY = 'text'
HUB = 'rlm/rag-prompt-llama'

def create_vectorestore():
    """
    Функция создания векторного хранилища.
    Анализируются текстовые файлы в каталоге text, результаты сохраняются в ChromaDb.
    """

    # читаем найстройки для Ollama
    settings = service.load_settings()
    ollama_settings = settings.get('ollama')
    if ollama_settings is not None:
        url = ollama_settings.get('base_url')
        model = ollama_settings.get('model')
        
        # загружаем все текстовые файлы из каталога text
        loader = DirectoryLoader(
            path=TEXT_DIRECTORY,
            glob="**/*.txt",
            recursive=True,
            loader_cls=TextLoader,
            loader_kwargs={'autodetect_encoding': True}
        )
        data = loader.load()

        # разбиваем документы на части для последующей векторизации
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=20)
        all_splits = text_splitter.split_documents(data)

        # создаем объект OllamaEmbeddings для обработки частей документов
        oembed = OllamaEmbeddings(base_url=url, model=model)

        # с помощью OllamaEmbeddings и векторной СУБД Chroma
        # из частей документов создаем векторное хранилище
        Chroma.from_documents(
            documents=all_splits,
            embedding=oembed,
            persist_directory=VECTORESTORE_DIRECTORY
        )

def search_docs(question: str) -> str:
    """
    Функция выполняет поиск документов соответствующих запросу.

    Параметры:
        question (str): запрос пользователя

    Возвращаемое значение:
        str: список документов в формате JSON.
    """

    # читаем найстройки для Ollama
    settings = service.load_settings()
    ollama_settings = settings.get('ollama')
    if ollama_settings is not None:
        url = ollama_settings.get('base_url')
        model = ollama_settings.get('model')

        # создаем объект OllamaEmbeddings для поиска частей документов
        # таким же способом как проводили векторизацию
        oembed = OllamaEmbeddings(base_url=url, model=model)

        # получаем объект векторной СУБД Chroma по каталогу, в который
        # ранее сохранили векторизованные документы
        vectorstore = Chroma(
            embedding_function=oembed,
            persist_directory=VECTORESTORE_DIRECTORY
        )

        # ищем похожие на запрос документы
        docs = vectorstore.similarity_search(question)
        return str(docs)

def chain_prompt(question: str) -> str:
    """
    Функция формирует ответ на основании запроса и контекста из найденных документов.
    Для формирования ответа используется Ollama.

    Параметры:
        question (str): запрос пользователя

    Возвращаемое значение:
        str: ответ пользователю.
    """

    # читаем найстройки для Ollama
    settings = service.load_settings()
    ollama_settings = settings.get('ollama')
    if ollama_settings is not None:
        url = ollama_settings.get('base_url')
        model = ollama_settings.get('model')

        # создаем объект Ollama для отправки запроса к модели
        ollama = Ollama(
            base_url=url,
            model=model,
            temperature=0.1,
            verbose=True
        )

        # создаем объект OllamaEmbeddings для поиска частей документов
        # таким же способом как проводили векторизацию
        oembed = OllamaEmbeddings(base_url=url, model=model)

        # получаем объект векторной СУБД Chroma по каталогу, в который
        # ранее сохранили векторизованные документы
        vectorstore = Chroma(
            embedding_function=oembed,
            persist_directory=VECTORESTORE_DIRECTORY
        )

        # ищем похожие на запрос документы
        docs = vectorstore.similarity_search(question)

        # получаем шаблон запроса из хаба
        QA_CHAIN_PROMPT = hub.pull(HUB)

        # создаем объект RetrievalQA для формирования ответа
        qa_chain = RetrievalQA.from_chain_type(
            ollama,
            retriever=vectorstore.as_retriever(),
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )

        # формируем ответ на запрос
        answer = qa_chain({"query": question})

        # логируем для анализа ответов
        logger.info(f'question: {question}\ndocs: {docs}\nanswer: {answer}')

        # возвращаем результат
        return answer.get('result')
