# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KitapyurduItem(scrapy.Item):
    # Kitap bilgilerini saklamak için field'ları tanımlıyoruz
    title = scrapy.Field()          # Kitap adı
    author = scrapy.Field()         # Yazar adı
    publisher = scrapy.Field()      # Yayınevi
    price = scrapy.Field()          # Fiyat
    original_price = scrapy.Field() # İndirim öncesi fiyat (varsa)
    discount = scrapy.Field()       # İndirim oranı (varsa)
    rating = scrapy.Field()         # Kitap puanı (varsa)
    image_url = scrapy.Field()      # Kitap kapak resmi URL'i
    book_url = scrapy.Field()       # Kitap detay sayfası URL'i
