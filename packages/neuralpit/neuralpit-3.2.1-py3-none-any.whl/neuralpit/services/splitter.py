import json
from typing import Any, Optional, List
from langchain.docstore.document import Document
from typing import Any, Dict, List
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter


class NeuralPitDocumentSplitter():

    def split_tika_text(self, text: str, source: any) -> List[Document]:
        """Converts a string or list of strings to a list of Documents with metadata."""
        soup = BeautifulSoup(text, features="lxml")
        pages = [page.get_text() for page in soup.find_all("div", {"class": "page"})]
        return self.page_to_docs(pages, source)

    def split_json_text(self, text: str) -> List[Document]:
        """Converts a string or list of strings to a list of Documents with metadata."""
        docs = json.loads(text)
        return [Document(page_content=doc['page_content'],metadata=doc['metadata']) for doc in docs]

    def page_to_docs(self, pages, source) -> List[Document]:
        docs = []
        for pIdx,page in enumerate(pages):
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=10000,
                separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
                chunk_overlap=0,
            )
            chunks = text_splitter.split_text(page)
            metadata = [{"source":source, "page": pIdx+1, "chunk": cIdx+1} for cIdx, _ in enumerate(chunks)]
            docs += [Document(page_content=p,metadata=m) for p,m in zip(chunks, metadata)]
        return docs