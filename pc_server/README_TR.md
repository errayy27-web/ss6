# SS OIL SQL Salt Okuma Servisi

**Önemli:** Telefonun SQL Server'a doğrudan bağlanması yerine Windows bilgisayarda bu servis çalışır. SQL Server'a kesinlikle INSERT/UPDATE/DELETE gönderilmez. SQL kullanıcısına yalnızca `SELECT` izni verin. SQL parolasını APK içine yazmayın.

## Gerekenler
- Windows bilgisayar ile telefon aynı yerel ağda olmalı.
- Python 3 ve `pip install pyodbc`.
- SQL Server 2005 ile uyumlu ODBC sürücüsü. Güncel sürücülerin SQL Server 2005 desteği garanti değildir; bilgisayarınızda uygun sürücü doğrulanmalıdır.
- Bilgisayarın IP adresi (örnek 192.168.100.50), port 8765; Windows güvenlik duvarında yalnızca yerel ağ için izin.

## Ayarlar (PowerShell örneği)
```
$env:SSOIL_API_TOKEN='BURAYA_UZUN_RASTGELE_ANAHTAR'
$env:SSOIL_ODBC_CONNECTION='DRIVER={SQL Server};SERVER=192.168.100.50\SQLEXPRESS;DATABASE=SSOIL_26;UID=SADECE_OKUMA_KULLANICISI;PWD=PAROLA;APP=SSOIL_READONLY;'
python server.py
```
**Örnek değerler gerçek bağlantı ayarı değildir.** Sunucu örneği ve şema isimleri bilgisayarda doğrulanmalıdır. Servisi internete açmayın. HTTP yalnızca güvenilen yerel ağ içindir; tercihen VPN/TLS ve firewall kullanın.

## Uygulama
SQL Ayarları → `http://BILGISAYAR_IP:8765` ve API anahtarını girin → Stok Güncelle → barkod okut → Excel'e kaydet.

## Stok hesaplama uyarısı
`ART.Kolicina - SUM(SmP_S.Kolicina)` formülü uygulanır. SmP_S içinde ART stokuna zaten yansımış eski satışlar varsa stok yanlış çıkar. Gerçek tabloda satış kapsamını doğrulamadan üretimde kullanmayın.

## Şema doğrulama
`dbo.ART_BK` tablosunda barkodun gerçekten `BKod_ID` alanında saklandığını ve `dbo.SmP_S` tablosunda `Kolicina` değerlerinin stoktan düşülecek satışlar olduğunu doğrulayın. Görsel ekran görüntüsü tüm veri türlerini doğrulamaz.
