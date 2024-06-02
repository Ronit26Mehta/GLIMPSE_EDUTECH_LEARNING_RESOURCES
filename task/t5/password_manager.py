import base64
import csv
import os

class AuthenticationError(Exception):
    pass

class PasswordManager:
    def __init__(self, master_password):
        self.master_password = master_password
        self.passwords = {}
        self.csv_file = 'passwords.csv'
        self.load_passwords()

    def authenticate(self, master_password):
        if master_password != self.master_password:
            raise AuthenticationError("Authentication failed. Incorrect master password.")

    def load_passwords(self):
        if os.path.exists(self.csv_file):
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    website = row['website']
                    username = row.get('username', '')
                    encrypted_password = row.get('encrypted_password', '')
                    decrypted_password = self.decrypt(encrypted_password)
                    self.passwords[website] = {'username': username, 'encrypted_password': encrypted_password, 'decrypted_password': decrypted_password}

    def save_passwords(self):
        with open(self.csv_file, 'w', newline='') as file:
            fieldnames = ['website', 'username', 'encrypted_password']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for website, credentials in self.passwords.items():
                writer.writerow({'website': website, 'username': credentials['username'], 'encrypted_password': credentials['encrypted_password']})

    def add_password(self, website, username, password, master_password):
        self.authenticate(master_password)
        encrypted_password = self.encrypt(password)
        self.passwords[website] = {'username': username, 'encrypted_password': encrypted_password, 'decrypted_password': password}
        self.save_passwords()

    def retrieve_password(self, website, master_password):
        self.authenticate(master_password)
        return self.passwords.get(website, None)

    def update_password(self, website, username, password, master_password):
        self.authenticate(master_password)
        if website in self.passwords:
            encrypted_password = self.encrypt(password)
            self.passwords[website] = {'username': username, 'encrypted_password': encrypted_password, 'decrypted_password': password}
            self.save_passwords()
        else:
            raise ValueError("Website not found.")

    def delete_password(self, website, master_password):
        self.authenticate(master_password)
        if website in self.passwords:
            del self.passwords[website]
            self.save_passwords()
        else:
            raise ValueError("Website not found.")

    def encrypt(self, password):
        # Simple encryption using base64 encoding
        return base64.b64encode(password.encode()).decode()

    def decrypt(self, encrypted_password):
        # Simple decryption using base64 decoding
        return base64.b64decode(encrypted_password).decode()

def display_menu():
    print("\nPassword Manager Menu:")
    print("1. Add Password")
    print("2. Retrieve Password")
    print("3. Update Password")
    print("4. Delete Password")
    print("5. Exit")

def main():
    master_password = input("Enter master password: ")
    password_manager = PasswordManager(master_password)

    try:
        password_manager.authenticate(master_password)
    except AuthenticationError as e:
        print(e)
        return

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            website = input("Enter website: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            master_password = input("Enter master password: ")
            try:
                password_manager.add_password(website, username, password, master_password)
                print("Password added successfully.")
            except AuthenticationError as e:
                print(e)
        elif choice == '2':
            website = input("Enter website: ")
            master_password = input("Enter master password: ")
            try:
                credentials = password_manager.retrieve_password(website, master_password)
                if credentials:
                    print(f"Username: {credentials['username']}")
                    print(f"Encrypted Password: {credentials['encrypted_password']}")
                    print(f"Decrypted Password: {credentials['decrypted_password']}")
                else:
                    print("Password not found.")
            except AuthenticationError as e:
                print(e)
        elif choice == '3':
            website = input("Enter website: ")
            username = input("Enter new username: ")
            password = input("Enter new password: ")
            master_password = input("Enter master password: ")
            try:
                password_manager.update_password(website, username, password, master_password)
                print("Password updated successfully.")
            except (AuthenticationError, ValueError) as e:
                print(e)
        elif choice == '4':
            website = input("Enter website: ")
            master_password = input("Enter master password: ")
            try:
                password_manager.delete_password(website, master_password)
                print("Password deleted successfully.")
            except (AuthenticationError, ValueError) as e:
                print(e)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
