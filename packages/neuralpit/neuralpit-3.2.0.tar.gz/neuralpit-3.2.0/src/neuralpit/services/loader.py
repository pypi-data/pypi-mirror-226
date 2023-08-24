import io
from pathlib import Path as p
from langchain.docstore.document import Document
from typing import Any, Dict, List
import fitz
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.document_loaders import UnstructuredWordDocumentLoader
from langchain.document_loaders import UnstructuredCSVLoader
from langchain.document_loaders import UnstructuredExcelLoader
from langchain.document_loaders import UnstructuredODTLoader
from langchain.document_loaders import UnstructuredEPubLoader
from langchain.document_loaders import UnstructuredEmailLoader
from langchain.document_loaders import UnstructuredImageLoader
from langchain.document_loaders import UnstructuredXMLLoader
from langchain.document_loaders import UnstructuredPowerPointLoader
from langchain.document_loaders import UnstructuredRSTLoader
from langchain.document_loaders import UnstructuredRTFLoader
from langchain.document_loaders import JSONLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import UnstructuredTSVLoader
from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import TomlLoader
from langchain.document_loaders import YoutubeLoader
from scrapy.crawler import CrawlerProcess
import io
from urllib.parse import urlparse
import mimetypes
from tempfile import NamedTemporaryFile
import pandas as pd
import boto3
import scrapy
import scrapy.crawler as crawler
from scrapy.utils.log import configure_logging
from multiprocessing import Process, Queue
from twisted.internet import reactor
from neuralpit.utils.webscrpper import LinksSpider
from neuralpit.utils.misc import text_from_html
from .splitter import NeuralPitDocumentSplitter


s3 = boto3.client('s3')
splitter = NeuralPitDocumentSplitter()

def load_pdf_file(tmp_file, source) -> List[Document]:
    doc = fitz.open(tmp_file)
    pages = [page.get_text() for page in doc]
    return splitter.page_to_docs(pages, source)

def load_word_file(tmp_file, source) -> List[Document]:
    loader = UnstructuredWordDocumentLoader(tmp_file.name, mode="elements", strategy="fast")
    docs = loader.load()
    content = [doc.page_content for doc in docs]
    return splitter.page_to_docs(content, source)

def load_text_file(tmp_file, source) -> List[Document]:
    loader = TextLoader(tmp_file.name)
    docs = loader.load()
    content = [doc.page_content for doc in docs]
    return splitter.page_to_docs(content, source)

def load_html_file(tmp_file, source) -> List[Document]:
    loader = UnstructuredHTMLLoader(tmp_file.name, mode="elements", strategy="fast")
    docs = loader.load()
    content = [doc.page_content for doc in docs]
    return splitter.page_to_docs(content, source)

def load_csv_file(tmp_file, source) -> List[Document]:
    loader = UnstructuredCSVLoader(tmp_file.name, mode="elements", strategy="fast")
    docs = loader.load()
    content = [doc.page_content for doc in docs]
    return splitter.page_to_docs(content, source)

def load_excel_file(tmp_file, source) -> List[Document]:
    loader = UnstructuredExcelLoader(tmp_file.name, mode="elements", strategy="fast")
    docs = loader.load()
    content = [doc.page_content for doc in docs]
    return splitter.page_to_docs(content, source)

def load_odt_file(tmp_file, source) -> List[Document]:
    loader = UnstructuredODTLoader(tmp_file.name, mode="elements", strategy="fast")
    docs = loader.load()
    content = [doc.page_content for doc in docs]
    return splitter.page_to_docs(content, source)

def load_epub_file(tmp_file, source) -> List[Document]:
    loader = UnstructuredEPubLoader(tmp_file.name, mode="elements", strategy="fast")
    docs = loader.load()
    content = [doc.page_content for doc in docs]
    return splitter.page_to_docs(content, source)

def load_email_file(tmp_file, source) -> List[Document]:
    loader = UnstructuredEmailLoader(tmp_file.name, mode="elements", strategy="fast")
    docs = loader.load()
    content = [doc.page_content for doc in docs]
    return splitter.page_to_docs(content, source)

def load_image_file(tmp_file, source) -> List[Document]:
    loader = UnstructuredImageLoader(tmp_file.name, mode="elements", strategy="fast")
    docs = loader.load()
    content = [doc.page_content for doc in docs]
    return splitter.page_to_docs(content, source)

def load_xml_file(tmp_file, source) -> List[Document]:
    loader = UnstructuredXMLLoader(tmp_file.name, mode="elements", strategy="fast")
    docs = loader.load()
    content = [doc.page_content for doc in docs]
    return splitter.page_to_docs(content, source)

def load_powerpoint_file(tmp_file, source) -> List[Document]:
    loader = UnstructuredPowerPointLoader(tmp_file.name, mode="elements", strategy="fast")
    docs = loader.load()
    content = [doc.page_content for doc in docs]
    return splitter.page_to_docs(content, source)

def load_rst_file(tmp_file, source) -> List[Document]:
    loader = UnstructuredRSTLoader(tmp_file.name, mode="elements", strategy="fast")
    docs = loader.load()
    content = [doc.page_content for doc in docs]
    return splitter.page_to_docs(content, source)

def load_rtf_file(tmp_file, source) -> List[Document]:
    loader = UnstructuredRTFLoader(tmp_file.name, mode="elements", strategy="fast")
    docs = loader.load()
    content = [doc.page_content for doc in docs]
    return splitter.page_to_docs(content, source)

def load_tsv_file(tmp_file, source) -> List[Document]:
    loader = UnstructuredTSVLoader(tmp_file.name, mode="elements", strategy="fast")
    docs = loader.load()
    content = [doc.page_content for doc in docs]
    return splitter.page_to_docs(content, source)

def load_json_file(tmp_file, source) -> List[Document]:
    loader = JSONLoader(tmp_file.name)
    docs = loader.load()
    content = [doc.page_content for doc in docs]
    return splitter.page_to_docs(content, source)

def load_toml_file(tmp_file, source) -> List[Document]:
    loader = TomlLoader(tmp_file.name)
    docs = loader.load()
    content = [doc.page_content for doc in docs]
    return splitter.page_to_docs(content, source)

class NeuralPitFileLoader():

    def __init__(self):
        self._mime_handlers = {}
        self._mime_handlers['application/pdf'] = load_pdf_file
        self._mime_handlers['application/vnd.openxmlformats-officedocument.wordprocessingml.document'] = load_word_file
        self._mime_handlers['application/msword'] = load_word_file
        self._mime_handlers['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'] = load_excel_file
        self._mime_handlers['application/vnd.ms-excel'] = load_excel_file
        self._mime_handlers['application/vnd.openxmlformats-officedocument.presentationml.presentation'] = load_powerpoint_file
        self._mime_handlers['application/vnd.ms-powerpoint'] = load_powerpoint_file
        self._mime_handlers['text/plain'] = load_text_file
        self._mime_handlers['text/html'] = load_html_file
        self._mime_handlers['text/csv'] = load_csv_file
        self._mime_handlers['application/vnd.oasis.opendocument.text'] = load_odt_file
        self._mime_handlers['application/epub+zip'] = load_epub_file
        self._mime_handlers['image/png'] = load_image_file
        self._mime_handlers['image/jpg'] = load_image_file
        self._mime_handlers['application/vnd.apple.installer+xml'] = load_xml_file
        self._mime_handlers['application/rtf'] = load_rtf_file
        self._mime_handlers['application/json'] = load_json_file
        self._mime_handlers['application/ld+json'] = load_json_file

        self._ext_handlers = {}
        self._ext_handlers['pdf'] = load_pdf_file
        self._ext_handlers['doc'] = load_word_file
        self._ext_handlers['docx'] = load_word_file
        self._ext_handlers['txt'] = load_text_file
        self._ext_handlers['html'] = load_html_file
        self._ext_handlers['xhtml'] = load_html_file
        self._ext_handlers['htm'] = load_html_file
        self._ext_handlers['csv'] = load_csv_file
        self._ext_handlers['xls'] = load_excel_file
        self._ext_handlers['xlsx'] = load_excel_file
        self._ext_handlers['xlsd'] = load_excel_file
        self._ext_handlers['odt'] = load_odt_file
        self._ext_handlers['epub'] = load_epub_file
        self._ext_handlers['eml'] = load_email_file
        self._ext_handlers['msg'] = load_email_file
        self._ext_handlers['png'] = load_image_file
        self._ext_handlers['jpg'] = load_image_file
        self._ext_handlers['xml'] = load_xml_file
        self._ext_handlers['ppt'] = load_powerpoint_file
        self._ext_handlers['pptx'] = load_powerpoint_file
        self._ext_handlers['rst'] = load_rst_file
        self._ext_handlers['rtf'] = load_rtf_file
        self._ext_handlers['json'] = load_json_file
        self._ext_handlers['jsonld'] = load_json_file
        self._ext_handlers['tsv'] = load_tsv_file
        self._ext_handlers['toml'] = load_toml_file

    def load(self,bucket,key) -> List[Document]:
        handler = None
        file_ext = key.split('.')[-1]
        if file_ext in self._ext_handlers:
            handler = self._ext_handlers[file_ext]
        if not handler:
            file_type = mimetypes.guess_type(key)[0]
            if file_type in self._handlers:
                handler = self._mime_handlers[file_type]
        if not handler:
            raise Exception("Unsupported file type ", key)

        source = dict(bucket=bucket, key = key, source = 's3')
        source_obj = s3.get_object(Bucket=bucket, Key=key)
        obj_content = source_obj['Body'].read()
        temp = NamedTemporaryFile(delete=False)
        with open(temp.name,'wb') as f:
            f.write(obj_content);
            f.close()
            return handler(temp, source)

class NeuralPitUrlLoader():

    def __init__(self):
        self.docs = []
        self.url = None

    def addLink(self, link,html):
        source = dict(url=self.url, link = link, source = 'url')
        page_content = text_from_html(html)
        docs = splitter.page_to_docs([page_content], source)
        self.docs.extend(docs)

    def load(self, url, mode):
        self.url = url
        self.docs = []
        if mode == 'single':
            domain = urlparse(url).netloc
            if domain =='youtube.com' or domain =='www.youtube.com':
                loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
                return loader.load()
            else:
                loader = WebBaseLoader(url)
                return loader.load()
        if mode == 'recursive':
            process = CrawlerProcess()
            process.crawl(LinksSpider, url=url, callback=self.addLink)
            process.start()
            return self.docs
        
    def run_spider(q):
        try:
            runner = crawler.CrawlerRunner()
            deferred = runner.crawl(LinksSpider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)
        
def load_csv_dataset(source_obj):
    return pd.read_csv(io.BytesIO(source_obj))

def load_excel_dataset(source_obj):
    return pd.read_excel(io.BytesIO(source_obj))

class NeuralPitDataframeLoader():

    def __init__(self):
        self._mime_handlers = {}
        self._mime_handlers['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'] = load_excel_dataset
        self._mime_handlers['application/vnd.ms-excel'] = load_excel_dataset
        self._mime_handlers['text/csv'] = load_csv_dataset

        self._ext_handlers = {}
        self._ext_handlers['csv'] = load_csv_dataset
        self._ext_handlers['xls'] = load_excel_dataset
        self._ext_handlers['xlsx'] = load_excel_dataset
        self._ext_handlers['xlsd'] = load_excel_dataset

    def load(self,bucket,key):
        handler = None
        file_ext = key.split('.')[-1]
        if file_ext in self._ext_handlers:
            handler = self._ext_handlers[file_ext]
        if not handler:
            file_type = mimetypes.guess_type(key)[0]
            if file_type in self._handlers:
                handler = self._mime_handlers[file_type]
        if not handler:
            raise Exception("Unsupported file type ", key)

        source_obj = s3.get_object(Bucket=bucket, Key=key)
        obj_content = source_obj['Body'].read()
        return handler(obj_content)
