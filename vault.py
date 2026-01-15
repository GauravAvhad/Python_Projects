import os
from cryptography.fernet import Fernet  # Import the security tool

# --- 1. KEY MANAGEMENT (The "House Key") ---
# We need a key to lock and unlock data.
        
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
choice = input("Do you want to (1) Save a Secret or (2) Read Secrets? ")

if choice == "1":
    # --- CREATE / WRITE MODE ---
    secret = input("Enter the secret you want to lock: ")

    # 1. Encrypt the secret (Turn text -> Scrambled Bytes)
    encrypted_data = cipher.encrypt(secret.encode())

    # 2. Save it to the file
    with open("secrets.txt", "wb") as file:
       file.write(encrypted_data)

    print("✅ Success! Your secret has been encryped and saved.") 

elif choice == "2":
    # --- READ / DECRYPT MODE ---
    if os.path.exists("secrets.txt"):
        # 1. Read the scrambled bytes from the file
        with open("secrets.txt", "rb") as file:
           encrypted_data = file.read()

        # 2. Decrypt it! (Turn Bytes back into Text)
        try:
            decrypted_date = cipher.decrypt(encrypted_data).decode()
            print(f"🔓 Your Decrypted Secret is: {decrypted_date}")   
        except:
            print("❌ Error: Key mismatch. Cannot decrypt.")    

    else:
        print("❌ No secret file found yet.")        

else:
    print("Invalid choice. Please type 1 or 2.")        