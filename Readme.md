# Divxplanet Altyazi İndirme Aparati

- Görsel cümbüşüne bulaşmadan altyazı indirme hedesi.
- XBMC Subtitle eklentisine addon hazırlığı

## Gereksinimler

* Python 2.7 ( http://www.python.org/download/releases/2.7.3/ )
* BeautifulSoup 3 ( http://www.crummy.com/software/BeautifulSoup/ )
* Mechanize ( http://wwwsearch.sourceforge.net/mechanize/ )
* Unrar (http://www.rarlab.com/rar_add.htm)

### Gereksinimlerin Kurulumu

Akıl sağlığı açısından öncelikle *easy_install* kurunuz:
https://pypi.python.org/pypi/setuptools

Akabinde şu komutu çalıştırınız:

* Linux : `sudo easy_install beautifulsoup mechanize rarfile`
* Windows : `C:\Python27\Scripts\easy_install beautifulsoup mechanize rarfile`

## Kullanım

`python dpdl.py 'Dizi Adi' sezon_no bolum_no`

1. Olası dizi adresi seçenekleri listelenir. (Tek sonuç çıktıysa direkt olarak o dizi seçilir)
2. Diziye ait numara girilir.
3. İlgili bölüme ait altyazılar listelenir.
4. Altyazıya ait numara girilerek indirilir.

## Sorunlar

* XBMCye uyarlamak istediğimizde Rarfile eklentisi olmadigi icin ayrica eklemek gerekecek.
* Paket altyazılar handle edilmiyor.
* Film altyazıları handle edilmiyor.

## Olabilecekler

* Sickbeard icin bir eklenti yapilabilir.
