from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from typing import List
from langchain.docstore.document import Document
import qdrant_client
from neuralpit.utils.paramstore import LLM_PROFILE


class NeuralPitVectorStore():

    def __init__(self, url, port):
        self._url = url
        self._port = port
        self._qclient = qdrant_client.QdrantClient(url=url,port=port)


    def is_indexed(self, conversation):
        try:
            collection_id = conversation.get('id')
            self._qclient.get_collection(collection_id)
            return True
        except:
            return False

    def get_retreiver(self,conversation): 
        collection_id = conversation.get('id')
        embeddings = OpenAIEmbeddings(openai_api_key=conversation.get('openai_api_key'),
                                           model=LLM_PROFILE['MODEL'])
        qdrant = Qdrant(client=self._qclient, collection_name=collection_id, embeddings=embeddings)
        return qdrant.as_retriever(k=LLM_PROFILE['MAX_DOCUMENT_RETREIVER'])
    
    def clear(self,conversation):
        try:
            collection_id = conversation.get('id')
            self._qclient.delete_collection(collection_id)
        except:
            print('Fail to delete collection in Qdrant server' , collection_id)

    def similarity_search(self, question, conversation):
        try:
            collection_id = conversation.get('id')
            embeddings = OpenAIEmbeddings(openai_api_key=conversation.get('openai_api_key'),
                                            model=LLM_PROFILE['MODEL'])
            qdrant = Qdrant(client=self._qclient, collection_name=collection_id, embeddings=embeddings)
            return qdrant.similarity_search(question, k=LLM_PROFILE['MAX_DOCUMENT_RETREIVER'])
        except:
            return False

    def add_documents(self, docs:List[Document],conversation):
        collection_id = conversation.get('id')
        embeddings = OpenAIEmbeddings(openai_api_key=conversation.get('openai_api_key'),
                                        model=LLM_PROFILE['MODEL'])
        texts = [doc.page_content for doc in docs]
        metadata = [doc.metadata for doc in docs]
        if self.is_indexed(conversation):
            qdrant = Qdrant(client=self._qclient, collection_name=collection_id, embeddings=embeddings)
            qdrant.add_texts(texts=texts,metadatas=metadata, batch_size = 64)
        else:
            print('No such collection exist, create new collection ' , collection_id)
            Qdrant.from_texts(url=self._url,
                                port=self._port, 
                                texts=texts, 
                                metadatas = metadata, 
                                collection_name=collection_id, 
                                embedding=embeddings, 
                                batch_size = 64)
            
