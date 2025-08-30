from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"  # spider name
    quote_count = 1
    file = open("quotes_two.txt", "a", encoding="utf-8")
    allowed_domains = ["quotes.toscrape.com"]

    # gidilecek sayfalar
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        # "https://quotes.toscrape.com/page/2/", (link takip etmek için bunu yoruma alıp quote__count ile sayfa sayısını bulabiliriz)
    ]

    def open_spider(self, spider):
        # Dosyayı spider başında aç
        self.file = open("quotes_two.txt", "a", encoding="utf-8")

    def close_spider(self, spider):
        # Dosyayı spider sonunda kapat
        if hasattr(self, "file") and not self.file.closed:
            self.file.close()

    def parse(self, response):
        quotes = response.css("div.quote")
        for quote in quotes:
            text = quote.css("span.text::text").get()
            author = quote.css("small.author::text").get()
            tags = quote.css("div.tags a.tag::text").getall()

            self.file.write(" ***************************** Quote: " + str(self.quote_count) + " *******************************\n")
            self.file.write(f"Text: {text}\n")
            self.file.write(f"Author: {author}\n")
            self.file.write(f"Tags: {str(tags)}\n\n")
            self.quote_count += 1

        # Sonraki sayfaya gitmek için next_page linkini bul ve takip et
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_url = "https://quotes.toscrape.com"+next_page
            yield scrapy.Request(url=next_url, callback=self.parse)