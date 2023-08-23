import json
from pathlib import Path
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exporters import CsvItemExporter
import sys
import mimetypes
from urllib.parse import urlparse
from scrapy.utils.log import configure_logging
from multiprocessing import Process, Queue
from twisted.internet import reactor


class LinksSpider(scrapy.Spider):
    """
    A Scrapy spider that extracts the full content of a website, including internal web links.

    Attributes:
        name (str): The name of the spider.
    """

    name = "NeuralPitScapper"

    def __init__(self, *args, **kwargs):
        """
        Initialize the LinksSpider instance.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(LinksSpider, self).__init__(*args, **kwargs)
        self.domain = urlparse(kwargs.get('url')).netloc
        self.start_urls = [kwargs.get('url')]
        self.callback = kwargs.get('callback')
        self.link_dict = set()

    def parse(self, response):
        """
        Parse the response and extract the full content from the current page.

        Parameters:
            response (scrapy.http.Response): The response to parse.
        """
        # Extract the full content from the current page
        link = response.url
        is_internal = self.is_internal_link(link)
        mime_type = self.get_mime_type(link)
        if not len(response.body) or link in self.link_dict or not is_internal or mime_type !='link':
            return
        self.link_dict.add(link)
        content = response.text
        self.callback(link, content)
        yield {
            'url': response,
            'content': content
        }

        # Extract internal web links and follow them
        for link in response.css('a::attr(href)').getall():
            if link.startswith('/') or link.startswith('http://') or link.startswith('https://'):
                yield response.follow(link, callback=self.parse)

    def is_internal_link(self, link):
        """
        Check if a given link is an internal link.

        Parameters:
            link (str): The link to check.

        Returns:
            bool: True if the link is an internal link, False otherwise.
        """
        domain = urlparse(link).netloc
        return self.domain == domain


    def get_mime_type(self, link):
        """
        Get the MIME type of a given link based on its file extension.

        Parameters:
            link (str): The link to check.

        Returns:
            str: The MIME type of the link.
        """
        file_extension = Path(link).suffix
        mime_type, _ = mimetypes.guess_type(file_extension)

        return mime_type if mime_type else 'link'
    



