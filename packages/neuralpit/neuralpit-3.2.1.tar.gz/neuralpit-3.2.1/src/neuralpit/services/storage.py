import json
import time
from datetime import datetime
from langchain.docstore.document import Document
from urllib.parse import urlparse
import boto3

s3 = boto3.client('s3')

class NeuralPitFileDocumentStorage():

    def __init__(self, storage_bucket):
        self._storage_bucket = storage_bucket

    def is_exist(self,bucket:str, key:str):
        try:
            s3.head_object(Bucket=self._storage_bucket, Key=f"{bucket}/{key}.json")
            return True
        except Exception as exc:
            print(exc)
            return False

    def get_documents(self,bucket:str, key:str)->str:
        if not self.is_exist(bucket,key):
            return None
        source_obj = s3.get_object(Bucket=bucket, Key=key)
        metadata = s3.get_object_tagging(Bucket=self._storage_bucket, Key=f"{bucket}/{key}.json")
        tags = {tag['Key']:tag['Value'] for tag in metadata['TagSet'] }
        last_modified =  tags['Source-Timestamp'] if 'Source-Timestamp' in tags else None
        if source_obj['LastModified'].strftime("%y-%m-%d %H:%M:%S") == last_modified:
            cached_obj = s3.get_object(Bucket=self._storage_bucket, Key=f"{bucket}/{key}.json")
            obj_content = cached_obj['Body'].read()
            doc_json = json.loads(obj_content)
            return [Document(page_content=doc['page_content'], metadata=doc['metadata']) for doc in doc_json]
        return None
    
    def save_documents(self, bucket, key, docs):
        source_obj = s3.get_object(Bucket=bucket, Key=key)
        content = [dict(page_content=doc.page_content,metadata=doc.metadata) for doc in docs]
        s3.put_object(Bucket=self._storage_bucket, 
                      Key=f"{bucket}/{key}.json", 
                      Body = json.dumps(content),
                      Tagging=f'Source-Timestamp={source_obj["LastModified"].strftime("%y-%m-%d %H:%M:%S")}'
                    )
        
    def delete_document_source(self, bucket, key):
        s3.delete_object(Bucket=self._storage_bucket, 
                      Key=f"{bucket}/{key}.json")


class NeuralPitWebDocumentStorage():

    def __init__(self, storage_bucket):
        self._storage_bucket = storage_bucket

    def get_documents(self,url:str)->str:
        domain = urlparse(url).netloc
        cached_obj = s3.get_object(Bucket=self.storage_bucket, Key=f"{domain}.json")
        obj_content = cached_obj['Body'].read()
        doc_json = json.loads(obj_content)
        return [Document(page_content=doc['page_content'], metadata=doc['metadata']) for doc in doc_json]
    
    def save_documents(self, url: str, docs):
        domain = urlparse(url).netloc
        content = [dict(page_content=doc.page_content,metadata=doc.metadata) for doc in docs]
        s3.put_object(Bucket=self.storage_bucket, 
                      Key=f"{domain}.json", 
                      Body = json.dumps(content),
                    )
        
    def delete_document_source(self, url:str):
        domain = urlparse(url).netloc
        s3.delete_object(Bucket=self.storage_bucket, 
                      Key=f"{domain}.json")
    

class NeuralPitDocumentStorage():

    def __init__(self, storage_bucket):
        self._docFileStorage = NeuralPitFileDocumentStorage(storage_bucket)
        self._docWebStorage = NeuralPitWebDocumentStorage(storage_bucket)

    def get_documents(self,source)->str:
        if source['source'] =='s3':
            return self._docFileStorage.get_documents(source['bucket'],source['key'])
        if source['source'] =='url':
            return self._docWebStorage.get_documents(source['url'])
        return None
    
    def save_documents(self, source, docs):
        if source['source'] =='s3':
            self._docFileStorage.save_documents(source['bucket'],source['key'], docs)
        if source['source'] =='url':
            self._docWebStorage.save_documents(source['url'], docs)
        
    def delete_document_source(self, source):
        if source['source'] =='s3':
            self._docFileStorage.delete_document_source(source['bucket'],source['key'])
        if source['source'] =='url':
            self._docWebStorage.delete_document_source(source['url'])
