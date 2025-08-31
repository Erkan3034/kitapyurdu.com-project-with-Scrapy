# Scrapy Çalışma Notları

## İçindekiler
1. [Scrapy Nedir?](#scrapy-nedir)
2. [Proje Yapısı](#proje-yapısı)
3. [Scrapy Shell Kullanımı](#scrapy-shell-kullanımı)
4. [CSS ve XPath Seçiciler](#css-ve-xpath-seçiciler)
5. [Spider Oluşturma](#spider-oluşturma)
6. [Items ve Fields](#items-ve-fields)
7. [Pipelines](#pipelines)
8. [Settings Ayarları](#settings-ayarları)
9. [Komutlar](#komutlar)
10. [İpuçları ve Best Practices](#ipuçları-ve-best-practices)

## Scrapy Nedir?

Scrapy, Python ile yazılmış güçlü bir web scraping framework'üdür. Web sitelerinden veri çıkarma, API'ler oluşturma ve veri madenciliği için kullanılır.

### Temel Özellikler:
- Asenkron ve hızlı
- Built-in veri export desteği (JSON, CSV, XML)
- Middleware ve pipeline sistemi
- Güçlü seçici desteği (CSS ve XPath)
- Otomatik robots.txt kontrolü

## Proje Yapısı

```
tutorial/
    scrapy.cfg            # deploy konfigürasyon dosyası
    tutorial/             # Python modülü
        __init__.py
        items.py          # proje items tanımları
        middlewares.py    # proje middlewares
        pipelines.py      # proje pipelines
        settings.py       # proje ayarları
        spiders/          # spider'ları koyacağınız dizin
            __init__.py
            quotes_spyder.py
```

## Scrapy Shell Kullanımı

Scrapy shell, web sayfalarını test etmek için interaktif bir ortamdır.

### Shell'i Başlatma:
```bash
# Boş shell
scrapy shell

# URL ile shell

scrapy shell 'https://quotes.toscrape.com/page/1/'

# Yerel dosya ile shell
scrapy shell file:///path/to/quotes-1.html
```

### Shell Komutları:

```python
# Response objesi hakkında bilgi
response
response.status
response.headers
response.url
response.text[:100]  # İlk 100 karakter

# Sayfa başlığını alma
response.css('title::text').get()
response.xpath('//title/text()').get()

# CSS seçiciler
response.css('h1').get()                    # İlk h1 elementi
response.css('h1').getall()                 # Tüm h1 elementleri
response.css('h1::text').get()              # h1 text içeriği
response.css('a::attr(href)').getall()      # Tüm link href'leri

# XPath seçiciler
response.xpath('//h1').get()                # İlk h1 elementi
response.xpath('//h1/text()').get()         # h1 text içeriği
response.xpath('//a/@href').getall()        # Tüm link href'leri

# Alıntıları çıkarma örneği (quotes.toscrape.com için)
quotes = response.css('div.quote')
for quote in quotes:
    text = quote.css('span.text::text').get()
    author = quote.css('small.author::text').get()
    tags = quote.css('div.tags a.tag::text').getall()
    print(f'Text: {text}')
    print(f'Author: {author}')
    print(f'Tags: {tags}')
    print('---')
```

### Response Metodları:

```python
# Tek element alma
response.css('title::text').get()           # İlk sonuç
response.css('title::text').get(default='') # Default değer ile

# Tüm elementleri alma
response.css('a::text').getall()            # Liste olarak tüm sonuçlar

# Re (regex) kullanımı
response.css('title::text').re(r'Quotes.*')
response.css('title::text').re_first(r'(\w+)')

# Follow links
response.follow('/page/2/', callback=self.parse)
response.follow(response.css('a.next'), callback=self.parse)
```

## CSS ve XPath Seçiciler

### CSS Seçiciler:

```python
# Element seçimi
response.css('div')                  # div elementleri
response.css('div.quote')            # quote class'ı olan div'ler
response.css('#main')                # main id'si olan element
response.css('div > p')              # div'in direkt alt p elementleri
response.css('div p')                # div içindeki tüm p elementleri

"""
# örnek sorgu:
>>> response.css('div.name.ellipsis a span::text').extract()

sorgu sonucu:

['Telefon Melefon Yok', 'Sarı Yüz', 'Basit Türkiye Tarihi', 'Engereğin Gözü', 'Biomortem / Glia', 'Robonlar 2 / Bir Hayal Operasyonu', 'Gökyüzünde Nehirler Var', 'Güneşsiz 1: Cehennem Diskosu', 'Erişkin Acil Servis Order-Reçete El Kitabı', 'Robonlar / Bir Kaçış Operasyonu', 'Saatleri Ayarlama Enstitüsü', 'Anne Terliği', 'Gece Yarısı Kütüphanesi', 'Pediatrik Acil Servis Order-Reçete El Kitabı ', 'El Kızı', 'Atomik Alışkanlıklar', 'Martin Eden', 'Yaşamak', 'Hapı Yuttuk Eczanesi', 'Kalk Bi Dopamin Demle']
>>> 

"""


# Attribute seçimi
response.css('a::attr(href)')        # href attribute'u
response.css('img::attr(src)')       # src attribute'u
response.css('div::attr(class)')     # class attribute'u

# Text içeriği
response.css('p::text')              # p elementinin text içeriği
response.css('div::text')            # Sadece direkt text

# Pseudo-selectors
response.css('li:first-child')       # İlk li elementi
response.css('li:last-child')        # Son li elementi
response.css('li:nth-child(2)')      # 2. li elementi
```


### XPath Seçiciler:

```python
# Element seçimi
response.xpath('//div')              # Tüm div elementleri
response.xpath('//div[@class="quote"]')  # quote class'ı olan div'ler
response.xpath('//div[@id="main"]')  # main id'si olan div
response.xpath('//div/p')            # div'in direkt alt p elementleri
response.xpath('//div//p')           # div içindeki tüm p elementleri

# Attribute seçimi
response.xpath('//a/@href')          # href attribute'ları
response.xpath('//img/@src')         # src attribute'ları

# Text içeriği
response.xpath('//p/text()')         # p elementinin text içeriği
response.xpath('//div//text()')      # div içindeki tüm text'ler

# Koşullu seçim
response.xpath('//div[contains(@class, "quote")]')  # class'ında quote geçen div'ler
response.xpath('//a[contains(text(), "Next")]')     # text'inde Next geçen linkler
response.xpath('//span[@class="text" and @itemprop="text"]')  # Çoklu koşul
```

### Karşılaştırma Tablosu:

| İşlem | CSS | XPath |
|-------|-----|-------|
| Class seçimi | `.quote` | `//*[@class="quote"]` |
| ID seçimi | `#main` | `//*[@id="main"]` |
| Attribute | `::attr(href)` | `/@href` |
| Text | `::text` | `/text()` |
| Contains | N/A | `[contains(@class, "quote")]` |
| Parent seçimi | N/A | `/..` |
| Following sibling | `~ element` | `/following-sibling::element` |

## Spider Oluşturma

### Basit Spider Örneği:

```python
import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/page/1/']

    def parse(self, response):
        # Alıntıları çıkar
        quotes = response.css('div.quote')
        
        for quote in quotes:
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
        
        # Sonraki sayfaya git
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

### Gelişmiş Spider Örneği:

```python
import scrapy
from tutorial.items import QuoteItem

class AdvancedQuotesSpider(scrapy.Spider):
    name = 'advanced_quotes'
    allowed_domains = ['quotes.toscrape.com']
    
    def start_requests(self):
        urls = [
            'https://quotes.toscrape.com/page/1/',
            'https://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        quotes = response.css('div.quote')
        
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.css('span.text::text').get()
            item['author'] = quote.css('small.author::text').get()
            item['tags'] = quote.css('div.tags a.tag::text').getall()
            
            # Yazar detay sayfasına git
            author_url = quote.css('small.author ~ a::attr(href)').get()
            if author_url:
                yield response.follow(
                    author_url, 
                    self.parse_author, 
                    meta={'item': item}
                )
            else:
                yield item
        
        # Pagination
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
    
    def parse_author(self, response):
        item = response.meta['item']
        item['author_birth_date'] = response.css('span.author-born-date::text').get()
        item['author_birth_location'] = response.css('span.author-born-location::text').get()
        item['author_description'] = response.css('div.author-description::text').get()
        yield item
```

## Items ve Fields

### Items Tanımlama:

```python
# items.py
import scrapy

class QuoteItem(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    author_birth_date = scrapy.Field()
    author_birth_location = scrapy.Field()
    author_description = scrapy.Field()

class AuthorItem(scrapy.Item):
    name = scrapy.Field()
    birth_date = scrapy.Field()
    birth_location = scrapy.Field()
    description = scrapy.Field()
```

### Item Kullanımı:

```python
def parse(self, response):
    item = QuoteItem()
    item['text'] = response.css('span.text::text').get()
    item['author'] = response.css('small.author::text').get()
    item['tags'] = response.css('div.tags a.tag::text').getall()
    yield item
```

## Pipelines

### Basit Pipeline:

```python
# pipelines.py
class TutorialPipeline:
    def process_item(self, item, spider):
        # Item işleme mantığı
        return item

class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['text'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item['text']}")
        else:
            self.ids_seen.add(item['text'])
            return item

class ValidateItemPipeline:
    def process_item(self, item, spider):
        if item.get('text') and item.get('author'):
            return item
        else:
            raise DropItem("Missing text or author")
```

### Pipeline'ları Etkinleştirme:

```python
# settings.py
ITEM_PIPELINES = {
    'tutorial.pipelines.ValidateItemPipeline': 300,
    'tutorial.pipelines.DuplicatesPipeline': 400,
    'tutorial.pipelines.TutorialPipeline': 500,
}
```

## Settings Ayarları

### Önemli Settings:

```python
# settings.py

# Robot.txt'i kontrol et
ROBOTSTXT_OBEY = True

# Download delay (saniye)
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = 0.5

# Concurrent requests
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# AutoThrottle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# User Agent
USER_AGENT = 'tutorial (+http://www.yourdomain.com)'

# Headers
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

# Export encoding
FEED_EXPORT_ENCODING = 'utf-8'

# Cache
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600
```

## Komutlar

### Proje Oluşturma:
```bash
scrapy startproject tutorial
cd tutorial
scrapy genspider quotes quotes.toscrape.com
```

### Spider Çalıştırma:
```bash
# Basit çalıştırma
scrapy crawl quotes

# Output dosyası ile
scrapy crawl quotes -o quotes.json
scrapy crawl quotes -o quotes.csv
scrapy crawl quotes -o quotes.xml

# Loglevel ayarlama
scrapy crawl quotes -L INFO
scrapy crawl quotes -L DEBUG
scrapy crawl quotes -L ERROR

# Custom settings
scrapy crawl quotes -s DOWNLOAD_DELAY=2
```

### Diğer Komutlar:
```bash
# Mevcut spider'ları listele
scrapy list

# Proje ayarlarını göster
scrapy settings

# Spider'ı kontrol et
scrapy check quotes

# Scrapy versiyonu
scrapy version

# Yardım
scrapy --help
```

## İpuçları ve Best Practices

### 1. Debugging:
```python
# Scrapy shell ile test
scrapy shell 'https://quotes.toscrape.com'

# Response'u kaydet
def parse(self, response):
    with open('debug.html', 'w') as f:
        f.write(response.text)
```

### 2. Error Handling:
```python
def parse(self, response):
    try:
        title = response.css('title::text').get()
        if not title:
            self.logger.warning(f'No title found on {response.url}')
    except Exception as e:
        self.logger.error(f'Error parsing {response.url}: {e}')
```

### 3. Custom Headers:
```python
def start_requests(self):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    for url in self.start_urls:
        yield scrapy.Request(url, headers=headers)
```

### 4. Cookies ve Sessions:
```python
def parse(self, response):
    # Login formu
    return scrapy.FormRequest.from_response(
        response,
        formdata={'username': 'admin', 'password': 'secret'},
        callback=self.parse_after_login
    )
```

### 5. Retry ve Error Handling:
```python
# settings.py
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]
```

### 6. Media Pipeline:
```python
# settings.py
ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
}
IMAGES_STORE = 'images'
```

### 7. Proxy Kullanımı:
```python
def start_requests(self):
    for url in self.start_urls:
        yield scrapy.Request(
            url,
            meta={'proxy': 'http://proxy.example.com:8080'}
        )
```

### 8. Memory Usage Optimization:
```python
# settings.py
MEMDEBUG_ENABLED = True
MEMUSAGE_ENABLED = True
MEMUSAGE_LIMIT_MB = 2048
```

## Örnek Projeler

### 1. E-ticaret Sitesi Scraping:
```python
class ProductSpider(scrapy.Spider):
    name = 'products'
    
    def parse(self, response):
        products = response.css('div.product')
        
        for product in products:
            yield {
                'name': product.css('h2.title::text').get(),
                'price': product.css('span.price::text').re_first(r'[\d.]+'),
                'image': product.css('img::attr(src)').get(),
                'url': response.urljoin(product.css('a::attr(href)').get()),
            }
```

### 2. Haber Sitesi Scraping:
```python
class NewsSpider(scrapy.Spider):
    name = 'news'
    
    def parse(self, response):
        articles = response.css('article')
        
        for article in articles:
            article_url = article.css('h2 a::attr(href)').get()
            yield response.follow(article_url, self.parse_article)
    
    def parse_article(self, response):
        yield {
            'title': response.css('h1::text').get(),
            'content': '\n'.join(response.css('div.content p::text').getall()),
            'date': response.css('time::attr(datetime)').get(),
            'author': response.css('span.author::text').get(),
        }
```

Bu notlar Scrapy'nin temel ve ileri düzey özelliklerini kapsamaktadır. Her zaman resmi Scrapy dokümantasyonunu kontrol etmeyi unutmayın: https://docs.scrapy.org/
