import requests
import os
import cloudscraper

from scrapy.http import HtmlResponse
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

SEARCH_QUERY_PREFIX = "what is "

class WebCrawler():
    def __init__(self):
        self.subscription_key = os.getenv('BING_SEARCH_V7_SUBSCRIPTION_KEY')
        self.endpoint = os.getenv('BING_SEARCH_V7_ENDPOINT') + "/v7.0/search"
    
    def crawl_asset_description(self, asset_name):
        converted_asset_name = ''.join([i for i in asset_name if not i.isdigit()])

        # Query term(s) to search for. 
        query = SEARCH_QUERY_PREFIX + converted_asset_name

        # Construct a request
        mkt = 'en-US'
        params = { 'q': query, 'mkt': mkt }
        headers = { 'Ocp-Apim-Subscription-Key': self.subscription_key }

        # Call the API
        try:
            response = requests.get(self.endpoint, headers=headers, params=params)
            response.raise_for_status()
            response_json = response.json()
            # pprint(response_json)

            pages = response_json["webPages"]["value"]

            urls = self.get_url_list(pages)
            for url in urls:
                description = self.get_website_content(url)
                if description != "":
                    break

            return description
        except Exception as ex:
            raise ex

    def get_url_list(self, pages):
        url_list_first = list()
        url_list_last = list()

        for page in pages:
            if "what is" in page["name"].lower():
                url_list_first.append(page["url"])
            else:
                url_list_last.append(page["url"])
        
        combinded_list = list()
        combinded_list.extend(url_list_first)
        combinded_list.extend(url_list_last)

        return combinded_list

    def get_website_content(self, url):
        try:
            response = requests.get(url, timeout=10)
            webpage = response.text
            # scraper = cloudscraper.create_scraper()
            # scraper.timeout = 10
            # webpage = scraper.get(url).text

            html_response = HtmlResponse(url=url, body=webpage, encoding='utf8')
            description = ''.join(html_response.selector.xpath("//p//text()").extract()).strip()
            
            return description
        except:
            return ""