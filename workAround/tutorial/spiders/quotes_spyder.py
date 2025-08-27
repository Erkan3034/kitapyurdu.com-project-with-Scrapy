from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes" # spider name

    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]



    """def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    """
    def parse(self, response):
        quotes = response.css("div.quote")
        title = quotes.css("span.text::text").extract_first() # get the text of the quote
        author = quotes.css("small.author::text").extract_first() # get the author of the quote
        tags = quotes.css("div.tags a.tag::text").extract_first() # get the tags of the quote
        yield { # yield the data to the pipeline 
            "title": title,
            "author": author,
            "tags": tags,
        }



# run the spider()