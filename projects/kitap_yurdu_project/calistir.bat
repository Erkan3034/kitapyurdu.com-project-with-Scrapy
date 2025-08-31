@echo off
echo Kitapyurdu En Cok Satan Kitaplar Spider'i Baslatiliyor...
echo.
cd kitapYurdu
scrapy crawl kitap_yurdu
echo.
echo Spider tamamlandi! Kitaplar.json ve kitaplar.csv dosyalari olusturuldu.
pause
