#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json

# Kitapyurdu'nun HTML yapısını analiz etmek için basit bir script
url = 'https://www.kitapyurdu.com/index.php?route=product/best_sellers&list_id=1'

print("Kitapyurdu HTML yapısını analiz ediyoruz...")

try:
    # Sayfa içeriğini al
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print(f"Sayfa başlığı: {soup.title.string if soup.title else 'Bulunamadı'}")
        
        # Farklı selector'ları test edelim
        selectors_to_test = [
            'div.product-cr',
            'div.product',
            'div.product-item',
            '.product-list .product',
            '.product-wrapper',
            '.book-item',
            '.product-card',
            'div[class*="product"]',
            '.item',
            '.list-item'
        ]
        
        print("\n=== SELECTOR TESTLERİ ===")
        for selector in selectors_to_test:
            elements = soup.select(selector)
            print(f"{selector}: {len(elements)} element bulundu")
            if elements:
                # İlk elementin class'larını göster
                first_element = elements[0]
                classes = first_element.get('class', [])
                print(f"  İlk elementin class'ları: {classes}")
                
                # İçindeki metin parçalarını göster
                text = first_element.get_text(strip=True)[:100]
                print(f"  İçerik örneği: {text}...")
                print("  ---")
        
        # Sayfa kaynağının bir kısmını dosyaya kaydet
        with open('kitapyurdu_source.html', 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        print("\nSayfa kaynağı 'kitapyurdu_source.html' dosyasına kaydedildi.")
        
        # Kitap isimlerini içeren elementleri bul
        print("\n=== KİTAP İSİMLERİNİ ARAMA ===")
        possible_title_selectors = [
            'a[title]',
            'h3 a',
            'h4 a', 
            '.name a',
            '.title a',
            '.product-name a',
            '.book-title a'
        ]
        
        for selector in possible_title_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"{selector}: {len(elements)} element")
                for i, elem in enumerate(elements[:3]):  # İlk 3 tanesini göster
                    title = elem.get('title') or elem.get_text(strip=True)
                    if title and len(title) > 5:  # Anlamlı başlık varsa
                        print(f"  {i+1}. {title}")
                print("  ---")
    
    else:
        print(f"Hata: HTTP {response.status_code}")
        
except Exception as e:
    print(f"Hata oluştu: {e}")
