import scrapy
from kitapYurdu.items import KitapyurduItem

class KitapYurduSpider(scrapy.Spider):
    name = 'kitap_yurdu'
    allowed_domains = ['kitapyurdu.com']
    
    # En çok satan kitaplar sayfasından başlıyoruz
    # Bu URL Kitapyurdu'nun en çok satanlar listesini gösteriyor
    start_urls = [
        'https://www.kitapyurdu.com/index.php?route=product/best_sellers&list_id=1'
    ]

    # Toplam kaç sayfa işleyeceğimizi kontrol etmek için sayaç
    max_books = 100
    books_scraped = 0

    def parse(self, response):
        """
        Ana parse fonksiyonu - en çok satanlar sayfasını işler
        Bu fonksiyon her kitap için detay bilgileri toplar
        """
        
        # Sayfadaki tüm kitapları buluyoruz
        # Kitapyurdu'da kitaplar genellikle 'product-cr' class'ı ile işaretlenir
        books = response.css('div.product-cr')
        
        # Eğer kitap bulunamazsa alternatif selector'ları deneyelim
        if not books:
            books = response.css('div.product-list div.product')
        
        if not books:
            books = response.css('.product-item')
            
        # Debug için: kaç kitap bulduğumuzu loglayalım
        self.logger.info(f'Found {len(books)} books on this page')
        
        # Her kitap için bilgileri çıkarıyoruz
        for book in books:
            # Maksimum kitap sayısına ulaştıysak dur
            if self.books_scraped >= self.max_books:
                break
                
            # Yeni bir item objesi oluşturuyoruz
            item = KitapyurduItem()
            
            # Kitap adını alıyoruz - genellikle 'name' class'ında bulunur
            title_element = book.css('div.name a::text').get()
            if not title_element:
                title_element = book.css('.product-title a::text').get()
            if not title_element:
                title_element = book.css('h3 a::text').get()
            if not title_element:
                title_element = book.css('.name::text').get()
            
            item['title'] = title_element.strip() if title_element else 'N/A'
            
            # Yazar adını alıyoruz
            author_element = book.css('div.author a::text').get()
            if not author_element:
                author_element = book.css('.author::text').get()
            if not author_element:
                author_element = book.css('.author a::text').get()
            
            item['author'] = author_element.strip() if author_element else 'N/A'
            
            # Yayınevi bilgisini alıyoruz
            publisher_element = book.css('div.publisher a::text').get()
            if not publisher_element:
                publisher_element = book.css('.publisher::text').get()
            if not publisher_element:
                publisher_element = book.css('.publisher a::text').get()
            
            item['publisher'] = publisher_element.strip() if publisher_element else 'N/A'
            
            # Fiyat bilgisini alıyoruz
            price_element = book.css('div.price-new::text').get()
            if not price_element:
                price_element = book.css('.price .value::text').get()
            if not price_element:
                price_element = book.css('.price::text').get()
            if not price_element:
                price_element = book.css('.price-current::text').get()
            
            item['price'] = price_element.strip() if price_element else 'N/A'
            
            # İndirimli fiyat varsa eski fiyatı da alıyoruz
            original_price_element = book.css('div.price-old::text').get()
            if not original_price_element:
                original_price_element = book.css('.price-old::text').get()
            
            item['original_price'] = original_price_element.strip() if original_price_element else 'N/A'
            
            # İndirim oranını hesaplıyoruz
            if original_price_element and price_element:
                try:
                    # Fiyatlardan sadece sayısal değerleri çıkarıyoruz
                    # Türkiye'de virgül ondalık ayırıcısı olarak kullanılır
                    current_price_str = ''.join(c for c in price_element if c.isdigit() or c in ',.')
                    old_price_str = ''.join(c for c in original_price_element if c.isdigit() or c in ',.')
                    
                    current_price = float(current_price_str.replace(',', '.'))
                    old_price = float(old_price_str.replace(',', '.'))
                    
                    discount_percent = round(((old_price - current_price) / old_price) * 100, 1)
                    item['discount'] = f"%{discount_percent}"
                except Exception as e:
                    item['discount'] = 'N/A'
            else:
                item['discount'] = 'N/A'
            
            # Kitap puanını alıyoruz (varsa)
            rating_element = book.css('.rating .value::text').get()
            if not rating_element:
                rating_element = book.css('.star-rating::attr(title)').get()
            if not rating_element:
                rating_element = book.css('.rating::text').get()
            
            item['rating'] = rating_element.strip() if rating_element else 'N/A'
            
            # Kitap kapak resminin URL'ini alıyoruz
            image_url = book.css('img::attr(src)').get()
            if not image_url:
                image_url = book.css('.product-image img::attr(src)').get()
            
            if image_url and not image_url.startswith('http'):
                image_url = response.urljoin(image_url)
            item['image_url'] = image_url if image_url else 'N/A'
            
            # Kitap detay sayfasının URL'ini alıyoruz
            book_url = book.css('div.name a::attr(href)').get()
            if not book_url:
                book_url = book.css('.product-title a::attr(href)').get()
            if not book_url:
                book_url = book.css('h3 a::attr(href)').get()
            if not book_url:
                book_url = book.css('a::attr(href)').get()
            
            if book_url and not book_url.startswith('http'):
                book_url = response.urljoin(book_url)
            item['book_url'] = book_url if book_url else 'N/A'
            
            # Sadece geçerli başlığı olan kitapları kabul ediyoruz
            if item['title'] != 'N/A' and len(item['title']) > 1:
                # Kitap sayacını artırıyoruz
                self.books_scraped += 1
                
                # Item'i yield ediyoruz (Scrapy bu veriyi işleyecek)
                yield item
                
                # Log mesajı yazdırıyoruz
                self.logger.info(f'Scraped book {self.books_scraped}: {item["title"]}')
        
        # Eğer henüz yeterli kitap toplamadıysak bir sonraki sayfaya geçiyoruz
        if self.books_scraped < self.max_books:
            # Sonraki sayfa linkini buluyoruz
            next_page = response.css('a.next::attr(href)').get()
            if not next_page:
                next_page = response.css('.pagination .next a::attr(href)').get()
            if not next_page:
                next_page = response.css('a[rel="next"]::attr(href)').get()
            
            # Eğer direkt link bulamazsak sayfa numarası ile deniyoruz
            if not next_page:
                current_page = response.meta.get('page', 1)
                next_page_num = current_page + 1
                # Maksimum 10 sayfa kontrol edelim (genellikle yeterli olur)
                if next_page_num <= 10:
                    next_page = f'https://www.kitapyurdu.com/index.php?route=product/best_sellers&list_id=1&page={next_page_num}'
            
            if next_page:
                self.logger.info(f'Following next page: {next_page}')
                # Sonraki sayfaya istek gönderiyoruz
                yield response.follow(next_page, 
                                    callback=self.parse, 
                                    meta={'page': response.meta.get('page', 1) + 1})
            else:
                self.logger.info('No more pages found or max pages reached')
    
    def parse_book(self, response):
        """
        Tekil kitap detay sayfasını işler (şu an kullanılmıyor ama gelecekte genişletilebilir)
        Eğer her kitap için daha detaylı bilgi toplamak isterseniz bu fonksiyon kullanılabilir
        """
        pass

    def parse_author(self, response):
        """
        Yazar detay sayfasını işler (şu an kullanılmıyor ama gelecekte genişletilebilir)
        Yazar hakkında ek bilgi toplamak için kullanılabilir
        """
        pass