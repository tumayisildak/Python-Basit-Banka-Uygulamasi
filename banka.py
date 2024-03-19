#Tümay Işıldak 
#20360859071

class Account:  #hesap sınıfı oluşturma
    def __init__(self, account_type, account_name, initial_balance):
        self._account_type = account_type
        self._account_name = account_name
        self._balance = 0   #baslangic bakiyesi 0 
        self.balance = initial_balance

    @property
    def account_type(self):
        return self._account_type

    @property
    def account_name(self):
        return self._account_name

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0: 
            raise ValueError("Hata: Bakiye negatif olamaz!")
        else:
            self._balance = value

    def paraGuncelle(self, transaction):#para cekme ve yatirmaya göre para guncelleme
        if isinstance(transaction, Transaction):
            if transaction.amount > 0:
                # Para çekme işlemi
                withdrawn_amount = transaction.paraCek()
                if self.balance - withdrawn_amount < 0:
                    raise ValueError("Hata: Yetersiz bakiye!")
                else:
                    self.balance = self.balance - withdrawn_amount
                    print(f"{self.account_name} hesabından {abs(withdrawn_amount)} TL çekildi. Yeni bakiye: {self.balance} TL")
            elif transaction.amount < 0:
                # Para ekleme işlemi
                deposited_amount = transaction.paraEkle()
                self.balance = self.balance - deposited_amount
                print(f"{self.account_name} hesabına {abs(deposited_amount)} TL eklendi. Yeni bakiye: {self.balance} TL")
            else:
                raise ValueError("Hata: Geçersiz işlem miktarı!")
        else:
            raise TypeError("Hata: Geçersiz Transaction nesnesi!")
    
    def close_account(self,hesap_tipi):#hesap silme
        
        if hesap_tipi =="Saving":
            SavingAccount.close_account(self)
           
       
        elif hesap_tipi=="Normal":
            NormalAccount.close_account(self)


class SavingAccount(Account):
    def close_account(self):
        closing_fee_percentage = 0.10 
        closing_fee = self.balance * closing_fee_percentage
        self.balance -= closing_fee #saving hesap kapatıldığında bakiye %10 azalır
        print(f"Savings hesabınız kapatıldı. Hesap adı: {self.account_name}, Kapanma ücreti: {closing_fee} TL, Kalan bakiye: {self.balance} TL")


class NormalAccount(Account):
    def close_account(self):
        print(f"Normal hesabınız kapatıldı. Hesap adı: {self.account_name}, Bakiye: {self.balance} TL")


class Transaction:
    def __init__(self, affected_account, amount):
        self._affected_account = affected_account
        self._amount = amount

    @property
    def affected_account(self):
        return self._affected_account

    @property
    def amount(self):
        return self._amount

    def paraDondur(self):
        print(f"Transaction para donduruldu: {self.amount} TL")

    def paraCek(self):
        return self.amount

    def paraEkle(self):
        return self.amount
    
def hesapOlustur(accounts):
    try:
        account_name = input("Hesap İsmi: ") #hesap ismi alır
        
        # Aynı isme sahip hesap var mı kontrolü
        for account in accounts:
            if account.account_name == account_name:
                raise ValueError(f"Hata: '{account_name}' isimli bir hesap zaten mevcut!")

        account_type = input("Hesap Türü (Normal/Saving): ").capitalize() #hesap türü alır ve baş harfi büyütür.
        initial_balance = float(input("Başlangıç Bakiyesi: ")) #baslangic bakiyesi alır
        #baslangic bakiyesi kontrolu
        if initial_balance < 0:
            raise ValueError("Hata: Negatif para miktarı giremezsiniz!")
        #hesap turu kontrolu
        if account_type not in ["Normal", "Saving"]:
            raise ValueError("Hata: Geçersiz hesap türü!")

        if account_type == "Saving":
            account = SavingAccount(account_type, account_name, initial_balance)
        else:
            account = NormalAccount(account_type, account_name, initial_balance)

        accounts.append(account)
        print(f"{account_type} hesap oluşturuldu. Hesap adı: {account_name}, Başlangıç bakiyesi: {initial_balance} TL")
    except ValueError as e:
        print(e)

#hesabı kapama fonksiyonu
def hesapKapat(accounts):
    account_name = input("Kapatılacak Hesap İsmi: ")
    for account in accounts:    #kapanacak hesap varsa kaldırır. yoksa hata verir
        if account.account_name == account_name:
            account.close_account(account.account_type)
            accounts.remove(account)
            print(f"{account_name} hesabı kapatıldı.")
            return

    print(f"{account_name} isimli hesap bulunamadı.")
#para yatırma veya çekme fonksiyonu, is_withdraw parametresine göre yatırma veya çekme işlemi yapar
def paraCekYatir(accounts, is_withdraw):
    try:
        account_name, amount = input(f"Para {'Çek' if is_withdraw else 'Yatır'} için (örnek: HESAP_ADI:MİKTAR boşluk bırakmadan girilmelidir!): ").split(":")
        amount = float(amount.strip())
        
        for account in accounts:
            if account.account_name == account_name:
                transaction = Transaction(account, amount if is_withdraw else -amount)
                account.paraGuncelle(transaction)
                return

        print(f"{account_name} isimli hesap bulunamadı.")
    except ValueError as e:
        print(e)
#hesapları dosyadan okur
def hesapYukle():
    accounts = []
    try:
        with open("dosya.txt", "r") as file:
            for line in file:
                account_data = line.strip().split(',')
                if len(account_data) == 3:
                    account_name, account_type, balance = account_data
                    accounts.append(Account(account_type, account_name, float(balance)))
        print("Hesap bilgileri dosyadan yüklendi.")
    except FileNotFoundError:
        print("Dosya bulunamadı.")
    except Exception as e:
        print(f"Hata: {e}")
    
    return accounts
#hesapları dosyaya yazar
def hesapKaydet(accounts):
    try:
        with open("dosya.txt", "w") as file:
            for account in accounts:
                file.write(f"{account.account_name},{account.account_type},{account.balance}\n")
        print("Hesap bilgileri dosyaya kaydedildi.")
    except Exception as e:
        print(f"Hata: {e}")
#dosyadaki hesapları konsola yazar
def goster():
    with open("dosya.txt", 'r') as file:
        # Dosyanın içeriğini oku
        veriler = file.read()
        
        # İçeriği ekrana yaz
        print(veriler)
# menü işlemleri
def islemMenusu():
    accounts = hesapYukle()  # Program başlatıldığında hesap bilgilerini otomatik olarak yükle

    while True:
        print("\nİŞLEM MENÜSÜ")
        print("1. Hesap Oluştur")
        print("2. Hesap Kapat")
        print("3. Kaydet ve Yükle")
        print("4. Para Çek")
        print("5. Para Yatır")
        print("6. Göster")
        print("7. Çıkış")

        choice = input("Seçenek: ")

        if choice == "1":
            hesapOlustur(accounts)
        elif choice == "2":
            hesapKapat(accounts)
        elif choice == "3":
            hesapKaydet(accounts)  
            hesapYukle()  
        elif choice == "4":
            paraCekYatir(accounts, is_withdraw=True)
        elif choice == "5":
            paraCekYatir(accounts, is_withdraw=False)
        elif choice == "6":
            goster()
        elif choice == "7":
            print("Çıkış yapılıyor.")
            break
        else:
            print("Geçersiz seçenek! Lütfen tekrar deneyin.")

# İşlem menüsünü çağırma
islemMenusu()
