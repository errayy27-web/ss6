# SS OIL Windows EXE (Python kurmadan)

1. GitHub'a proje ZIP icindeki dosyalari yukleyin.
2. GitHub > Actions > **SS OIL Windows Server EXE** > Run workflow.
3. Basarili islemden **SS-OIL-Windows-Server-EXE** artifact'ini indirin, ZIP'ten cikarin.
4. AYARLAR_ORNEK.bat dosyasini AYARLAR.bat adi ile kopyalayin ve SQL okuma kullanicisi, parola ve API anahtari degerlerini doldurun.
5. BASLAT.bat dosyasina cift tiklayin. Pencere acik kaldigi surece servis calisir.
6. Telefonda `http://BILGISAYAR_IP:8765` ve ayni API anahtarini girin.

**Bilgisayara Python kurulmaz.** EXE, GitHub'in Windows bilgisayarinda olusturulur. Windows bilgisayarda SQL Server 2005 ile uyumlu ODBC surucusu bulunmasi gerekir. `DRIVER={SQL Server}` ancak bilgisayarda varsa calisir. Windows guvenlik duvarinda 8765 portunu sadece guvenilen yerel aga acin. API'yi internete acmayin.

**Guvenlik:** SQL hesabi yalniz SELECT yetkili olmalidir. AYARLAR.bat parolayi acik metin saklar: sadece yetkili kullanicilarin erisebilecegi klasorde tutun ve GitHub'a yuklemeyin.

**Stok dogrulugu:** ART.Kolicina'dan SmP_S'nin tum tarihsel satislarini cikarmak yanlis olabilir. Gece stok guncellemesine dahil edilen satislarin kesim noktasini teyit etmeden net stok sonucunu kullanmayin.
