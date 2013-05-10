# Divxplanet Altyazi İndirme Aparati

- Görsel cümbüşüne bulaşmadan altyazı indirme hedesi.
- XBMC Subtitle eklentisine addon hazırlığı

## Gereksinimler

* Python 2.7
* BeautifulSoup 3
* Mechanize
* Rarfile

--buralara kurulumla ilgili ufak tefek hedeler :) --

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
