import dotenv # Load environment variables from .env file

dotenv.load_dotenv() # Load environment variables from .env file

from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain # Import the correct module for combining documents
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder # Import the correct module for chat prompts
from langchain.memory import ChatMessageHistory # Import the correct module for chat message history
from langchain.vectorstores.faiss import FAISS # Import the correct module for FAISS vector store
from langchain.document_loaders.unstructured import UnstructuredFileLoader # Import the correct module for UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter # Import the correct module for text splitting
from langchain_openai import OpenAIEmbeddings # Import the correct module for OpenAI embeddings
from langchain_core.runnables import RunnablePassthrough # Import the correct module for runable passthrough
from langchain_core.output_parsers import StrOutputParser # Import the correct module for string output parser
from langchain_core.runnables import RunnableBranch # Import the correct module for runnable branch

import logging # Import logging module for logging

logging.basicConfig(level=logging.INFO) # Set logging level to INFO

logger = logging.getLogger(__name__) # Create a logger for this module

def parse_retriver_input(params):
    return params["message"][-1:].content # Extract the last message from the input parameters

class LoggerStrOutputParser(StrOutputParser):
    def parse(self, text: str) -> str:
        logger.info(f"Query: {text}") # it prints a message like Query: <your text> to the log. This helps you keep track of what text is being processed. For tracking
        return text # After logging the text, it returns the exact same text without any modifications.


class Chat:
    def __init__(self): # Initialize the Chat class
        self.history = {} 
        self.__init_chain()
        self.__init_retriever()
        self.__init_transformation_chain()
        self.retrieval_chain = ( # Initialize the retrieval chain
            RunnablePassthrough.assign(
                context=self.query_transforming_retriever_chain, # It assigns a component that processes the query
            ).assign(
                answer=self.chain, # It assigns a component that generates the answer based on the context
            )
        )

    
    def __init_chain(self): # Initialize the chain
        self.chat_api = ChatOpenAI( model= "gpt-3.5-turbo-0125", temperature= 0.2)# Create a ChatOpenAI instance
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a helpful assistant named Mahdi who has a PhD student in UoA. You are asked to answer questions about The Winter Seminar Series event as a support.
Winter Seminar Series is a professional community event hosted by the Sharif University of Technology, aimed at bringing together successful Iranians globally to focus on computer science and engineering topics. Established eight years ago by the Student Scientific Chapter, WSS has become a significant four-day event where speakers present their research, share findings, and teach. The seminar includes presentations, roundtable discussions on various scientific topics, and educational workshops. These workshops are conducted online by university alumni and cover practical aspects of computer science and engineering. The event also features roundtable discussions in Persian, encouraging networking and knowledge exchange among participants.
The user has asked a question about the event. 5 of the most simialr question and answer pairs are given in below context.
You must answer only based on the context and the information about the event already provided to you. try to give positive answers about the event.
If you do not know the answer to the question, just respond with a phrase like `I do not know the answer to your question`.
rewrite the question and answer pairs in the context to match the user's question.
here is the context:

{context}""",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        self.chain = create_stuff_documents_chain( self.chat_api,
            prompt=prompt
        ) # Create a chain for combining documents using the chat API and the prompt
    
    def __init_retriever(self):
        loader = UnstructuredFileLoader("datasets/Q&A.txt") # Load the dataset from a text file
        splitter = RecursiveCharacterTextSplitter(
            separators='\n\n',
            chunk_size=20,
            chunk_overlap=0,
            length_function=len,
        ) # Split the text into smaller chunks for processing
        documents = loader.load_and_split(splitter) # Load and split the documents
        vectorstore = FAISS.from_documents(documents, OpenAIEmbeddings()) # Create a FAISS vector store from the documents and embeddings
        loader = UnstructuredFileLoader("datasets/WSS.txt") # Load the dataset from a text file
        documents = loader.load_and_split(splitter) # Load and split the documents
        vectorstore.add_documents(documents) # Add the documents to the vector store
        self.retriever = vectorstore.as_retriever(k = 5) # Create a retriever from the vector store with a specified number of documents to retrieve
        logger.info("retriever initialized") # Log the initialization of the retriever

    def __init_transformation_chain(self):
        query_transform_prompt = ChatPromptTemplate.from_messages(
            [
                MessagesPlaceholder(variable_name="messages"),
                (
                    "user",
                    """Given the above conversation, generate a search query to look up in order to get relevant information to the conversation. Only respond with the query, nothing else. give a general query that doesn't contain specific keywords. as an example:
Winter Seminal Series WSS is an event, so questions regarding WSS should just give queries about event without containing the specific name of the event. here are some examples of user question and query pair:
user: when is WSS being held?
query: when is event being held?
user: I'm hungry?
query: where is food being served?"""
                ),
            ]
        )
        self.query_transforming_retriever_chain = RunnableBranch(
            (
                lambda x: len(x.get("messages", [])) == 1,
                query_transform_prompt | self.chat_api | LoggerStrOutputParser() | self.retriever,
            ),
            query_transform_prompt | self.chat_api | LoggerStrOutputParser() | self.retriever,
        ).with_config(run_name="chat_retriever_chain")

    def add_user(self, user):
        self.history[user] = ChatMessageHistory()
        logger.info(f"user {user} added")

    def has_user(self, user):
        return user in self.history # This method checks if the given user is already present in the history dictionary. In simple terms, it returns True if the user exists in self.history and False otherwise.
    

    def chat(self, user, message):
        if not self.has_user(user):
            self.add_user(user)
        logger.info(f"Q: {message}")
        self.history[user].add_user_message(message)
        response = self.retrieval_chain.invoke({"messages": self.history[user].messages})
        logger.info(f"A: {response}")
        self.history[user].add_ai_message(response['answer'])
        return response['answer']
    
    def count_message(self, user):
        return len(self.history[user].messages)
    