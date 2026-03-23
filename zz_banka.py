import random
from datetime import datetime

# Dil sözlüğü (i18n)
LANGUAGES = {
    "TR": {
        "welcome": "--- Banka Uygulamasına Hoş Geldiniz ---",
        "main_menu": "1. Hesap Oluştur\n2. Giriş Yap\n3. Çıkış",
        "choice": "Seçiminiz: ",
        "create_name": "Adınız ve Soyadınız: ",
        "acc_created": "Hesabınız başarıyla oluşturuldu! Hesap Numaranız: {}",
        "login_acc": "Hesap Numaranız: ",
        "login_success": "Giriş başarılı! Hoş geldin, {}.",
        "login_fail": "Hata: Hesap bulunamadı!",
        "user_menu": "\n--- İşlemler ---\n1. Bakiye Görüntüle\n2. Para Yatır\n3. Para Çek\n4. Para Transferi\n5. İşlem Geçmişi\n6. Çıkış Yap",
        "balance": "Mevcut Bakiyeniz: {:.2f} TL",
        "amount_deposit": "Yatırılacak miktar: ",
        "deposit_success": "{:.2f} TL yatırıldı. Yeni bakiye: {:.2f} TL",
        "amount_withdraw": "Çekilecek miktar: ",
        "withdraw_success": "{:.2f} TL çekildi. Yeni bakiye: {:.2f} TL",
        "insufficient": "Hata: Yetersiz bakiye!",
        "invalid_amount": "Hata: Geçersiz miktar girdiniz!",
        "transfer_target": "Transfer edilecek hesap numarası: ",
        "transfer_amount": "Transfer edilecek miktar: ",
        "transfer_success": "Transfer başarılı! Yeni bakiyeniz: {:.2f} TL",
        "transfer_fail": "Hata: Alıcı hesap bulunamadı veya kendi hesabınıza transfer yapamazsınız!",
        "history_title": "--- İşlem Geçmişi ---",
        "no_history": "Henüz bir işlem yapılmamış.",
        "invalid_choice": "Geçersiz seçim, lütfen tekrar deneyin.",
        "goodbye": "Bizi tercih ettiğiniz için teşekkürler. İyi günler!"
    },
    "EN": {
        "welcome": "--- Welcome to the Bank Application ---",
        "main_menu": "1. Create Account\n2. Login\n3. Exit",
        "choice": "Your choice: ",
        "create_name": "Your Full Name: ",
        "acc_created": "Account successfully created! Your Account Number: {}",
        "login_acc": "Account Number: ",
        "login_success": "Login successful! Welcome, {}.",
        "login_fail": "Error: Account not found!",
        "user_menu": "\n--- Operations ---\n1. View Balance\n2. Deposit\n3. Withdraw\n4. Transfer Money\n5. Transaction History\n6. Logout",
        "balance": "Current Balance: ${:.2f}",
        "amount_deposit": "Amount to deposit: ",
        "deposit_success": "${:.2f} deposited. New balance: ${:.2f}",
        "amount_withdraw": "Amount to withdraw: ",
        "withdraw_success": "${:.2f} withdrawn. New balance: ${:.2f}",
        "insufficient": "Error: Insufficient funds!",
        "invalid_amount": "Error: Invalid amount entered!",
        "transfer_target": "Target account number: ",
        "transfer_amount": "Amount to transfer: ",
        "transfer_success": "Transfer successful! New balance: ${:.2f}",
        "transfer_fail": "Error: Receiver account not found or cannot transfer to self!",
        "history_title": "--- Transaction History ---",
        "no_history": "No transactions yet.",
        "invalid_choice": "Invalid choice, please try again.",
        "goodbye": "Thank you for choosing us. Have a nice day!"
    }
}

class BankAccount:
    def __init__(self, name):
        self.name = name
        self.account_number = str(random.randint(10000, 99999))
        self.balance = 0.0
        self.history = []

    def add_history(self, transaction):
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"[{date_str}] {transaction}")

class BankApp:
    def __init__(self):
        self.accounts = {} # account_number: BankAccount object
        self.lang = "TR"
        self.t = LANGUAGES[self.lang]
        self.current_user = None

    def select_language(self):
        while True:
            print("Select Language / Dil Seçimi:")
            print("1. Türkçe (TR)")
            print("2. English (EN)")
            choice = input("1/2: ")
            if choice == "1":
                self.lang = "TR"
                break
            elif choice == "2":
                self.lang = "EN"
                break
            else:
                print("Invalid choice / Geçersiz seçim.\n")
        self.t = LANGUAGES[self.lang]

    def run(self):
        self.select_language()
        print(f"\n{self.t['welcome']}")

        while True:
            print("\n" + self.t['main_menu'])
            choice = input(self.t['choice'])

            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.login()
            elif choice == "3":
                print(self.t['goodbye'])
                break
            else:
                print(self.t['invalid_choice'])

    def create_account(self):
        name = input(self.t['create_name'])
        new_account = BankAccount(name)
        self.accounts[new_account.account_number] = new_account
        print(self.t['acc_created'].format(new_account.account_number))

    def login(self):
        acc_num = input(self.t['login_acc'])
        if acc_num in self.accounts:
            self.current_user = self.accounts[acc_num]
            print(self.t['login_success'].format(self.current_user.name))
            self.user_menu()
        else:
            print(self.t['login_fail'])

    def user_menu(self):
        while True:
            print(self.t['user_menu'])
            choice = input(self.t['choice'])

            if choice == "1": # Bakiye
                print(self.t['balance'].format(self.current_user.balance))
            elif choice == "2": # Para Yatır
                self.deposit()
            elif choice == "3": # Para Çek
                self.withdraw()
            elif choice == "4": # Transfer
                self.transfer()
            elif choice == "5": # İşlem Geçmişi
                self.show_history()
            elif choice == "6": # Çıkış
                self.current_user = None
                break
            else:
                print(self.t['invalid_choice'])

    def deposit(self):
        try:
            amount = float(input(self.t['amount_deposit']))
            if amount <= 0:
                print(self.t['invalid_amount'])
                return
            self.current_user.balance += amount
            msg = self.t['deposit_success'].format(amount, self.current_user.balance)
            print(msg)
            
            # Geçmişe ekle (Dile göre dinamik metin tutulabilir ama basitlik için direkt string ekliyoruz)
            action = f"Deposit: +{amount:.2f}" if self.lang == "EN" else f"Para Yatırma: +{amount:.2f}"
            self.current_user.add_history(action)
        except ValueError:
            print(self.t['invalid_amount'])

    def withdraw(self):
        try:
            amount = float(input(self.t['amount_withdraw']))
            if amount <= 0:
                print(self.t['invalid_amount'])
                return
            if amount > self.current_user.balance:
                print(self.t['insufficient'])
                return
            
            self.current_user.balance -= amount
            print(self.t['withdraw_success'].format(amount, self.current_user.balance))
            
            action = f"Withdraw: -{amount:.2f}" if self.lang == "EN" else f"Para Çekme: -{amount:.2f}"
            self.current_user.add_history(action)
        except ValueError:
            print(self.t['invalid_amount'])

    def transfer(self):
        target_acc = input(self.t['transfer_target'])
        if target_acc not in self.accounts or target_acc == self.current_user.account_number:
            print(self.t['transfer_fail'])
            return
            
        try:
            amount = float(input(self.t['transfer_amount']))
            if amount <= 0:
                print(self.t['invalid_amount'])
                return
            if amount > self.current_user.balance:
                print(self.t['insufficient'])
                return
                
            # Parayı gönderenden düş, alıcıya ekle
            self.current_user.balance -= amount
            self.accounts[target_acc].balance += amount
            print(self.t['transfer_success'].format(self.current_user.balance))
            
            # Gönderen geçmişi
            sender_action = f"Transfer to {target_acc}: -{amount:.2f}" if self.lang == "EN" else f"{target_acc} nolu hesaba transfer: -{amount:.2f}"
            self.current_user.add_history(sender_action)
            
            # Alıcı geçmişi
            receiver_action = f"Transfer from {self.current_user.account_number}: +{amount:.2f}" if self.lang == "EN" else f"{self.current_user.account_number} nolu hesaptan transfer: +{amount:.2f}"
            self.accounts[target_acc].add_history(receiver_action)
            
        except ValueError:
            print(self.t['invalid_amount'])

    def show_history(self):
        print("\n" + self.t['history_title'])
        if not self.current_user.history:
            print(self.t['no_history'])
        else:
            for record in self.current_user.history:
                print(record)

# Uygulamayı başlat
if __name__ == "__main__":
    app = BankApp()
    app.run()