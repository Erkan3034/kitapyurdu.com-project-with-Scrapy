# Kitapyurdu En Çok Satan Kitaplar Spider'ı

Bu Scrapy projesi Kitapyurdu.com sitesinden en çok satan 100 kitabın bilgilerini toplar ve dosyaya kaydeder.

## Kurulum

1. Scrapy kurulumu (eğer kurulu değilse):
```bash
pip install scrapy
```

## Nasıl Çalıştırılır

### Temel Kullanım

Spider'ı çalıştırmak için proje klasöründe şu komutu kullanın:

```bash
cd projects/kitap_yurdu_project/kitapYurdu
scrapy crawl kitap_yurdu
```

### Çıktı Dosyaları

Spider çalıştığında otomatik olarak şu dosyalar oluşturulur:
- `kitaplar.json` - JSON formatında kitap bilgileri
- `kitaplar.csv` - CSV formatında kitap bilgileri (Excel'de açılabilir)

### Manuel Çıktı Belirtme

Farklı dosya adı veya format kullanmak için:

```bash
# JSON çıktısı için
scrapy crawl kitap_yurdu -o kitaplar.json

# CSV çıktısı için
scrapy crawl kitap_yurdu -o kitaplar.csv

# Excel çıktısı için
scrapy crawl kitap_yurdu -o kitaplar.xlsx
```

## Toplanan Veriler

Her kitap için şu bilgiler toplanır:
- **title**: Kitap adı
- **author**: Yazar adı
- **publisher**: Yayınevi
- **price**: Güncel fiyat
- **original_price**: İndirim öncesi fiyat (varsa)
- **discount**: İndirim oranı (varsa)
- **rating**: Kitap puanı (varsa)
- **image_url**: Kapak resmi URL'i
- **book_url**: Kitap detay sayfası URL'i

## Önemli Notlar

- Spider maksimum 100 kitap toplar
- İstekler arasında 2 saniye bekleme süresi vardır (sitenin yoğunluğunu azaltmak için)
- Hatalı istekler otomatik olarak 3 kez tekrar denenir
- Çıktı dosyaları UTF-8 kodlamasında kaydedilir (Türkçe karakterler desteklenir)

## Sorun Giderme

Eğer spider çalışmazsa:

1. İnternet bağlantınızı kontrol edin
2. Kitapyurdu.com sitesinin erişilebilir olduğunu kontrol edin
3. Scrapy'nin doğru sürümünün kurulu olduğunu kontrol edin: `scrapy --version`

## Spider Mantığı

1. **Başlangıç**: En çok satanlar sayfasından başlar
2. **Veri Toplama**: Her kitap için belirlenen bilgileri toplar
3. **Sayfalama**: Sonraki sayfalara otomatik geçer
4. **Limit**: 100 kitaba ulaşınca durur
5. **Çıktı**: Toplanan verileri belirtilen dosyalara kaydeder
