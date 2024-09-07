# 📋 Proje Adı: **Telegram Haber Botu**

Telegram botu, belirli bir web sitesinden anlık haberleri tarayarak her yarım saatte bir haber gönderir.

## 🚀 Özellikler:
- **Web Scraping**: Web sayfalarındaki haber başlıklarını otomatik olarak tarar.
- **Telegram Bot Entegrasyonu**: Taranan haberler, Telegram botu aracılığıyla belirtilen bir kanala gönderilir.
- **Geri Sayım**: Bir sonraki haberin gönderilmesine kalan süreyi gösteren dinamik bir sayaç.
- **SQLite Veritabanı**: Önceden gönderilen haberler kaydedilir, böylece tekrar gönderilmez.

---

## 📦 Tanıtım

Bu proje, bir Telegram botu aracılığıyla **anlık haber gönderim sistemi** sunar. Web scraping tekniğiyle bir web sitesindeki haberler düzenli olarak kontrol edilir ve bu haberler, belirlenen bir Telegram kanalına otomatik olarak iletilir.

**Telegram Haber Botu**, her 30 dakikada bir yeni haberleri kontrol eder ve kanala paylaşır. Aynı zamanda, gönderilen haberlerin tekrar gönderilmesini önlemek için SQLite veritabanı kullanır. 

---

## 🚧 Gereksinimler

- **Python 3.7+**
- **Telegram Bot API Token** (Bot oluşturma adımları [burada](https://core.telegram.org/bots#3-how-do-i-create-a-bot))

---

## 🛠 Kullanılan Teknolojiler

- **Python**: Uygulamanın temel programlama dili.
- **Telegram Bot API**: Haberleri Telegram kanallarına göndermek için.

---

## 📷 Ekran Görüntüsü

![Ekran Görüntüsü](./Ekran%20görüntüsü%202024-09-07%20190428.png)

---
