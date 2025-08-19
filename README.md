# Library System
## Yasin Küçüker

Kütüphane yönetimi projesi. Bu proje, kullanıcıların kitap ekleyip silebileceği, kitapları listeleyebileceği bir terminal uygulaması ve FastAPI tabanlı bir web servisi sunar.  

Verileri ister konsol ekranında ekleyip listeleyebilir, isterseniz silebilirsiniz. Ayrıca Open Library Books API’den faydalanarak ISBN kodunu girdiğiniz kitabı kütüphanenize ekleyebilir, aynı şekilde listeleyebilir ve silebilirsiniz.

---

## 🖥 Console Ekranı

`OOP` klasörü içindeki `main.py` dosyasını çalıştırarak terminal üzerinden uygulamayı kullanabilirsiniz.

`Library` sınıfının fonksiyonları:

- `add_book()` → ISBN ile kitap ekler.  
- `remove_book()` → ISBN ile kitap siler.  
- `list_books()` → Kütüphanedeki tüm kitapları listeler.  
- `find_book()` → ISBN ile kitap arar.

---

## 📚 Open Library Books (OLB)

`OLB Api` klasörü altındaki `main.py` dosyasını çalıştırarak ISBN numarasını girdiğiniz kitabı [Open Library](https://openlibrary.org/) üzerinden çekebilirsiniz.

---

## 🌐 FAST API Web Servisi

1. `FAST Api` klasörü altına gidin.  
2. Terminal’den aşağıdaki komutu çalıştırarak FastAPI sunucusunu başlatın ve servisi ayağa kaldırın:

uvicorn api:app --reload

[FastAPI Dokümantasyonu](http://127.0.0.1:8000/docs) adresinden (http://127.0.0.1:8000/docs) girdiğiniz isbn kodu ile get put ve delete işlemlerini gerçekleştirebilirsiniz.

