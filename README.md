# Hermes Instagram

Amaç: Hermes'e **"Hermes Instagram görevi"** denildiğinde bu repodaki kod çalıştırılır.

## Akış
1. Google Drive'daki **Hermes Instagram / Videolar** klasörünü kontrol et.
2. Daha önce başarıyla Instagram'a yüklenen Drive dosya kimliklerini durum dosyasından oku.
3. Yalnızca yeni videoları sırayla işle.
4. Instagram yüklemesi gerçekten başarılı olduktan sonra video kimliğini `.hermes_instagram_state.json` içine kaydet.
5. Sonraki çalıştırmada eski videoları tekrar yükleme.
6. Yeni video yoksa hiçbir şey yapmadan çık.

## Drive klasörleri
- Proje: `Hermes Instagram` — `1SXaqtqMVNh8kfN200GNzEpgA3kid486m`
- Videolar: `Hermes Instagram/Videolar` — `14PBXxE_6fQrPHCvuZGYiZrecpWJ0759R`

Durum dosyası Drive'daki proje klasöründe tutulur. Böylece yeni Hermes oturumunda bile hangi videoların daha önce gönderildiği anlaşılır.

## Çalıştırma
```bash
pip install -r requirements.txt
python hermes_instagram.py
```

## API durumu
Drive tarama, video indirme ve tekrar-yüklemeyi önleme altyapısı hazırdır.

Instagram yayınlama fonksiyonu şimdilik kilitlidir. Meta/Instagram API kimlikleri oluşturulup test edildikten sonra `instagram_create_reel_from_local_file()` resmi yayınlama akışıyla etkinleştirilecektir. Başarısız yükleme "yayınlandı" olarak işaretlenmez.

## Hermes görevi
Hermes görev çağrıldığında repoyu günceller, ortam değişkenlerini yükler, `python hermes_instagram.py` çalıştırır ve sonucu kullanıcıya bildirir.

API anahtarları/tokenlar GitHub'a commit edilmemelidir.
