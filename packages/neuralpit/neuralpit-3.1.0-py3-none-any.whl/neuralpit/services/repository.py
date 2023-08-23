from typing import List
from datetime import date
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import uuid
import time

class OpenAIKeyRepository:
    def __init__(self, table) -> None:
        self.table = table

    def list_item(self):
        response = self.table.scan()
        items = response.get('Items', [])
        return [item['key'] for item in items]

class OpenAIUsageRepository:
    def __init__(self, table) -> None:
        self.table = table

    def create_item(self, conversation_id: str, api_key: str, context: any,  usage: any):
        timestamp = str(round(time.time()))
        id =  uuid.uuid4().hex 
        self.table.update_item(
            Key={'id': id},
            UpdateExpression="set conversation_id=:c, created_date=:d, openai_api_key=:k, context=:ctx, #usage=:u",
            ExpressionAttributeValues={
                ':c': conversation_id, ':k': api_key, ':d': timestamp, ':ctx': context, ':u':usage},
            ExpressionAttributeNames={
                "#usage": "usage",
            },
            ReturnValues="UPDATED_NEW")
        return id
    

class ConversationRepository:
    def __init__(self, table) -> None:
        self.table = table

    def create_item(self, conversation: any):
        timestamp = str(round(time.time()))
        id =  uuid.uuid4().hex if 'id' not in conversation else conversation['id']
        user_id = conversation['user_id']
        self.table.update_item(
            Key={'id': id},
            UpdateExpression="set user_id=:u, created_date=:d",
            ExpressionAttributeValues={
                ':u': user_id, ':d': timestamp},
            ReturnValues="UPDATED_NEW")
        return id
    
    def update_item_metadata(self, id: str, metadata: any):
        self.table.update_item(
            Key={'id': id},
            UpdateExpression="set #metadata=:m",
            ExpressionAttributeNames={
                "#metadata": "metadata"
            },
            ExpressionAttributeValues={ ':m': metadata},
            ReturnValues="UPDATED_NEW")
        return id

    def get_item(self, id:str):
        response = self.table.get_item(Key={'id': id})
        item = response.get('Item', {})
        return item
    
    def delete_item(self, id:str):
        self.table.delete_item(Key={'id': id})
        return True
    
class ConversationDocumentRepository:
    def __init__(self, table) -> None:
        self.table = table

    def create_item(self, conversation_id: str, source: any):
        timestamp = str(round(time.time()))
        id = uuid.uuid4().hex
        self.table.update_item(
            Key={'id': id},
            UpdateExpression="set conversation_id=:c, created_date=:d, #source=:s",
            ExpressionAttributeNames={
                "#source": "source",
            },
            ExpressionAttributeValues={
                ':c': conversation_id, ':s': source, ':d': timestamp},
            ReturnValues="UPDATED_NEW")
        return id
    
    def update_item(self, id: str, source: any):
        self.table.update_item(
            Key={'id': id},
            UpdateExpression="set #source=:s",
            ExpressionAttributeNames={
                "#source": "source"
            },
            ExpressionAttributeValues={ ':s': source},
            ReturnValues="UPDATED_NEW")
        return id
    
    def delete_item(self, id:str):
        self.table.delete_item(Key={'id': id})
        return True
    
    def delete_item_by_conversation_id(self, conversation_id:str):
        response = self.table.query(IndexName='conversation_id-index', 
                                    KeyConditionExpression=Key('conversation_id').eq(conversation_id) )
        items = response.get('Items', [])
        for item in items:
            self.table.delete_item(Key={'id': item.get('id')})
        return True
    
    def get_item_by_conversation_id(self, conversation_id:str):
        response = self.table.query(IndexName='conversation_id-index', 
                                    KeyConditionExpression=Key('conversation_id').eq(conversation_id) )
        items = response.get('Items')
        return items
    
    def get_item(self, id:str):
        response = self.table.get_item(Key={'id': id})
        item = response.get('Item', {})
        return item
    
    def update_summary(self, document_id: str, summary:str):
        self.table.update_item(
            Key={'id': document_id},
            UpdateExpression="set summary=:s",
            ExpressionAttributeValues={
                ':s': summary},
            ReturnValues="UPDATED_NEW")
        return id


class ConversationDatasourceRepository:
    def __init__(self, table) -> None:
        self.table = table

    def create_item(self, conversation_id: str, source: any, metadata: any):
        timestamp = str(round(time.time()))
        id = uuid.uuid4().hex
        self.table.update_item(
            Key={'id': id},
            UpdateExpression="set conversation_id=:c, created_date=:d, #source=:s, #metadata=:m",
            ExpressionAttributeNames={
                "#source": "source",
                "#metadata":"metadata"
            },
            ExpressionAttributeValues={
                ':c': conversation_id, ':s': source, ':m': metadata, ':d': timestamp},
            ReturnValues="UPDATED_NEW")
        return id
    
    def update_item(self, id: str, source: any, metadata: any):
        self.table.update_item(
            Key={'id': id},
            UpdateExpression="set #source=:s, #metadata=:m",
            ExpressionAttributeNames={
                "#source": "source",
                "#metadata":"metadata"
            },
            ExpressionAttributeValues={ ':s': source,':m': metadata},
            ReturnValues="UPDATED_NEW")
        return id
    
    def delete_item(self, id:str):
        self.table.delete_item(Key={'id': id})
        return True
    
    def delete_item_by_conversation_id(self, conversation_id:str):
        response = self.table.query(IndexName='conversation_id-index', 
                                    KeyConditionExpression=Key('conversation_id').eq(conversation_id) )
        items = response.get('Items', [])
        for item in items:
            self.table.delete_item(Key={'id': item.get('id')})
        return True
    
    def get_item_by_conversation_id(self, conversation_id:str):
        response = self.table.query(IndexName='conversation_id-index', 
                                    KeyConditionExpression=Key('conversation_id').eq(conversation_id) )
        items = response.get('Items')
        return items[0] if items else None
    
    def get_item(self, id:str):
        response = self.table.get_item(Key={'id': id})
        item = response.get('Item', {})
        return item


class ConversationHistoryRepository:
    def __init__(self, table) -> None:
        self.table = table

    def create_item(self, conversation_id: str, question: str, answer, reference, user_id: str):
        timestamp = str(round(time.time()))
        id = uuid.uuid4().hex
        self.table.update_item(
            Key={'id': id},
            UpdateExpression="set conversation_id=:c, created_date=:d, question=:q, answer=:a, #reference=:r, user_id=:u",
            ExpressionAttributeValues={
                ':c': conversation_id, ':q': question, ':d': timestamp, ':a': answer, ':r': reference, ':u': user_id},
            ExpressionAttributeNames={"#reference": "reference"},
            ReturnValues="UPDATED_NEW")
        return id
    
    def delete_item(self, id:str):
        self.table.delete_item(Key={'id': id})
        return True
    
    def delete_item_by_conversation_id(self, conversation_id:str):
        response = self.table.query(IndexName='conversation_id-index', 
                                    KeyConditionExpression=Key('conversation_id').eq(conversation_id) )
        items = response.get('Items', [])
        for item in items:
            self.table.delete_item(Key={'id': item.get('id')})
        return True
    
    def get_item_by_conversation_id(self, conversation_id:str):
        response = self.table.query(IndexName='conversation_id-index', 
                                    KeyConditionExpression=Key('conversation_id').eq(conversation_id) )
        items = response.get('Items', [])
        return items
    
    def get_item(self, id:str):
        response = self.table.get_item(Key={'id': id})
        item = response.get('Item', {})
        return item