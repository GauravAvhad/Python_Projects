import os
from cryptography.fernet import Fernet  # Import the security tool

# --- 1. KEY MANAGEMENT (The "House Key") ---
# 1. SETUP THE KEY
if not os.path.exists("my.key"):
    key = Fernet.generate_key()
    with open("my.key", "wb") as kf:
        kf.write(key)

# 2. Load the key
key = open("my.key", "rb").read()
cipher = Fernet(key) # This is the tool we will use to lock/unlock

# --- 3. THE MAIN MENU ---
print("\n--- 🔐 SECURE VAULT ---")
choice = input("Do you want to (1) Save, (2) Read, or (3) Delete Secrets? ")

if choice == "1":
    # --- CREATE / WRITE MODE (C in CRUD) ---
    secret = input("Enter the secret you want to lock: ")
    encrypted_data = cipher.encrypt(secret.encode())

    with open("secrets.txt", "wb") as file:
       file.write(encrypted_data)
    print("✅ Success! Your secret has been encryped and saved.") 

elif choice == "2":
    # --- READ / DECRYPT MODE (R in CRUD) ---
    if os.path.exists("secrets.txt"):
        with open("secrets.txt", "rb") as file:
           encrypted_data = file.read()
        try:
            decrypted_data = cipher.decrypt(encrypted_data).decode()
            print(f"🔓 Your Decrypted Secret is: {decrypted_data}")   
        except:
            print("❌ Error: Key mismatch. Cannot decrypt.")    
    else:
        print("❌ No secret file found yet.")        

elif choice == "3":
    # --- DELETE MODE (D in CRUD) ---
    if os.path.exists("secrets.txt"):
        confirm = input("⚠️ WARNING: Are you sure you want to delete all secrets? (y/n): ")
        if confirm.lower() == 'y':
            os.remove("secrets.txt")
            print("🗑️ Vault wiped! All secrets deleted securely.")
        else:
            print("Action canceled.")
    else:
        print("❌ Vault is already empty.")

else:
    print("Invalid choice. Please type 1, 2, or 3.")