from library import Library

def main():
    library = Library()

    while True:
        print("\n--- Kütüphane Menüsü ---")
        print("1. Kitap Ekle (ISBN ile)")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış")

        choice = input("Seçiminizi yapın: ")

        if choice == "1":
            isbn = input("ISBN girin: ")
            library.add_book(isbn)
        elif choice == "2":
            isbn = input("Silmek istediğiniz kitabın ISBN numarasını girin: ")
            library.remove_book(isbn)
        elif choice == "3":
            library.list_books()
        elif choice == "4":
            isbn = input("Aramak istediğiniz kitabın ISBN numarasını girin: ")
            book = library.find_book(isbn)
            print(book if book else "Kitap bulunamadı.")
        elif choice == "5":
            print("Çıkılıyor...")
            break
        else:
            print("Geçersiz seçim!")

if __name__ == "__main__":
    main()
