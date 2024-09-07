import requests
from bs4 import BeautifulSoup
import telegram
import asyncio
import time
import sqlite3

# Telegram bot token ve kanal kullanıcı adı
bot_token = "bot_token_giriniz"
channel_username = "@chat_id"  # Kanalın kullanıcı adı

# Hedef URL
url = "https://www.haberler.com/guncel/"  # Örnek bir sayfa

# SQLite veritabanı bağlantısı
conn = sqlite3.connect('sent_articles.db')
cursor = conn.cursor()

# Daha önce gönderilen haberleri tutacak tabloyu oluşturuyoruz
cursor.execute('''
CREATE TABLE IF NOT EXISTS sent_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    link TEXT UNIQUE
)
''')
conn.commit()

# Veritabanına daha önce gönderilen haberleri ekleme
def add_article_to_db(link):
    cursor.execute('INSERT OR IGNORE INTO sent_articles (link) VALUES (?)', (link,))
    conn.commit()

# Veritabanında daha önce gönderilmiş bir haber olup olmadığını kontrol etme
def is_article_in_db(link):
    cursor.execute('SELECT 1 FROM sent_articles WHERE link = ?', (link,))
    return cursor.fetchone() is not None

# Web scraping işlemi
def scrape_articles(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"URL'e erişilemedi. Durum Kodu: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # p12-col sınıfına sahip div'leri buluyoruz
    articles = soup.find_all('div', class_='p12-col')
    
    # Verileri depolamak için liste
    article_data = []
    
    for article in articles:
        # İçerisindeki a etiketini buluyoruz
        link_element = article.find('a', class_='hbBoxMainText')
        
        # a etiketini kontrol ediyoruz
        if link_element:
            # Href'i tam URL'ye dönüştürüyoruz
            link = "https://www.haberler.com" + link_element['href']
            title = link_element['title']
            
            # Verileri listeye ekliyoruz
            article_data.append({
                'title': title,
                'link': link
            })
    
    return article_data

# Telegram bot mesajı gönderme işlemi
async def send_telegram_message(article):
    try:
        # Her makale için Telegram mesajı oluşturuyoruz
        bot = telegram.Bot(token=bot_token)
        
        # Başlığı stilize ediyoruz (örn: büyük harf ve **kalın**)
        formatted_title = f"🔹 **{article['title'].upper()}**"
        
        # Mesajı hazırlıyoruz
        message = f"{formatted_title}\n\n🌐 [Habere Git]({article['link']})"
        
        # Telegram mesajını gönderme
        await bot.send_message(chat_id=channel_username, text=message, parse_mode='Markdown')
        print("Yeni haber gönderildi:", article['title'])
    
    except telegram.error.BadRequest as e:
        print(f"Mesaj gönderilemedi. Hata: {e}")
    except Exception as e:
        print(f"Hata: {e}")

# Konsolda zamanı göstermek için sayaç
def countdown(seconds):
    for remaining in range(seconds, 0, -1):
        print(f"{remaining} saniye kaldı...", end="\r", flush=True)
        time.sleep(1)

# Haberleri kontrol etme ve yeni haber bulunca Telegram'a gönderme işlemi
async def check_new_articles():
    articles = scrape_articles(url)
    
    if articles:
        for article in articles:
            # Eğer haber daha önce gönderilmemişse Telegram'a gönderiyoruz
            if not is_article_in_db(article['link']):
                await send_telegram_message(article)
                add_article_to_db(article['link'])  # Haberi veritabanına ekle

# İlk çalıştırmada haberleri yarım saat arayla gönderme
async def send_articles_with_delay():
    articles = scrape_articles(url)
    
    if articles:
        for article in articles:
            # Eğer haber daha önce gönderilmemişse Telegram'a gönderiyoruz
            if not is_article_in_db(article['link']):
                await send_telegram_message(article)
                add_article_to_db(article['link'])  # Haberi veritabanına ekle
                
                # Yarım saat (1800 saniye) bekleme ve zaman sayacı
                countdown(1800)

# Ana fonksiyon
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    
    # İlk olarak tüm haberleri yarım saat arayla gönderiyoruz
    loop.run_until_complete(send_articles_with_delay())
    
    # Sonrasında her 5 dakikada bir yeni haber olup olmadığını kontrol ediyoruz
    while True:
        loop.run_until_complete(check_new_articles())
        countdown(300)  # 5 dakika geri sayım
