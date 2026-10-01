# HERMES INSTAGRAM — ANA GÖREV

Bu repo, Hermes'e **"Instagram görevine başla"** denildiğinde çalıştırılacak görev tanımıdır.

## Amaç
Google Drive'daki **Hermes Instagram/Videolar** klasörünü kontrol et. Daha önce başarıyla paylaşılmamış en eski yeni videoyu bul, videoyu analiz et, İngilizce Instagram açıklaması ve tam 5 ilgili İngilizce hashtag hazırla ve Instagram'da gönderi/Reel olarak yayınla.

## Sabit Google Drive klasörleri
- Proje klasörü: `Hermes Instagram`
- Proje klasör ID: `1SXaqtqMVNh8kfN200GNzEpgA3kid486m`
- Video klasörü: `Hermes Instagram/Videolar`
- Video klasör ID: `14PBXxE_6fQrPHCvuZGYiZrecpWJ0759R`
- Durum dosyası: `.hermes_instagram_state.json`

## Her çalıştırmada yapılacaklar
1. Bu repoyu güncelle ve bu dosyayı oku.
2. Google Drive video klasörünü tara.
3. `.hermes_instagram_state.json` içindeki daha önce başarıyla yayınlanan Drive file ID'lerini oku.
4. Aynı Drive file ID daha önce başarıyla yayınlandıysa ASLA tekrar paylaşma.
5. Yeni video yoksa: **"Yeni video yok; işlem yapılmadı."** diye rapor ver ve çık.
6. Birden fazla yeni video varsa createdTime sırasına göre **en eski yeni videodan** başla. Varsayılan olarak bir çalıştırmada yalnızca 1 video yayınla.
7. Videoyu indir ve içeriğini gerçekten analiz et. Görüntüdeki ana konu, karakter, hareket ve sahneye göre kısa bir İngilizce caption yaz. Dosya adını körlemesine caption olarak kullanma.
8. Caption doğal ve kısa olsun; uydurma karakter/olay ekleme.
9. Caption sonuna tam **5 İngilizce hashtag** ekle. Hashtagler videoya uygun olsun. Anime/çizgi film içeriğinde uygun olduğunda örnek havuz: `#Anime #Cartoon #Animation #AnimatedSeries #Explore`. İçerik farklıysa hashtagleri içeriğe göre değiştir.
10. Instagram yayınlama API kimlikleri yoksa paylaşılmış gibi davranma; kullanıcıya hangi eksik kimliğin gerektiğini açıkça bildir.
11. Yayınlama gerçekten başarılı olduktan ve Instagram media ID döndükten SONRA Drive file ID'yi durum dosyasına kaydet.
12. Hata olursa video işlenmiş/yayınlanmış olarak işaretlenmeyecek. Sonraki çalıştırmada yeniden denenebilir.
13. Başarı sonunda video adı, caption, 5 hashtag ve Instagram media ID'yi kullanıcıya bildir.

## Güvenlik
- Token, client secret, şifre veya API anahtarını GitHub'a commit etme.
- Kimlikleri environment variable / Hermes secret store üzerinden al.
- Başarılı API yanıtı olmadan state dosyasını güncelleme.
- Aynı videoyu tekrar yayınlama.

## Gerekli ortam değişkenleri
Google Drive:
- `GOOGLE_SERVICE_ACCOUNT_FILE` veya `GOOGLE_OAUTH_TOKEN_FILE`
- `DRIVE_PROJECT_FOLDER_ID` (varsayılan repo kodunda tanımlı)
- `DRIVE_VIDEOS_FOLDER_ID` (varsayılan repo kodunda tanımlı)

Instagram:
- `IG_USER_ID`
- `IG_ACCESS_TOKEN`
- `GRAPH_VERSION`

## Hermes'e verilecek tek komut
**Instagram görevine başla. GitHub'daki benartcartoon/hermesinstagram reposunu güncelle, HERMES.md görevini aynen uygula.**
