"""
Author: [Leni]
Version: 1.0
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import tkinter as tk
from tkinter import messagebox

# AES256 Schlüssel generieren
def generate_key():
    return get_random_bytes(32)  # 256-bit Schlüssel

# Nachricht mit AES256 verschlüsseln
def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')

# Nachricht mit AES256 entschlüsseln
def decrypt_message(encrypted_message, key):
    try:
        encrypted_data = base64.b64decode(encrypted_message)
        nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
    except Exception as e:
        return f"Fehler: {str(e)}"

# GUI erstellen
def create_gui():
    def encrypt_action():
        message = message_entry.get()
        if not message:
            messagebox.showerror("Fehler", "Bitte eine Nachricht eingeben.")
            return
        encrypted = encrypt_message(message, key)
        encrypted_text.set(encrypted)
    
    def decrypt_action():
        encrypted_message = encrypted_text.get()
        if not encrypted_message:
            messagebox.showerror("Fehler", "Bitte eine verschlüsselte Nachricht eingeben.")
            return
        decrypted = decrypt_message(encrypted_message, key)
        decrypted_text.set(decrypted)
    
    root = tk.Tk()
    root.title("AES256 Crypto App")
    
    tk.Label(root, text="Nachricht:").pack()
    message_entry = tk.Entry(root, width=40)
    message_entry.pack()
    
    tk.Button(root, text="Verschlüsseln", command=encrypt_action).pack()
    
    encrypted_text = tk.StringVar()
    tk.Label(root, text="Verschlüsselte Nachricht:").pack()
    tk.Entry(root, textvariable=encrypted_text, width=50).pack()
    
    tk.Button(root, text="Entschlüsseln", command=decrypt_action).pack()
    
    decrypted_text = tk.StringVar()
    tk.Label(root, text="Entschlüsselte Nachricht:").pack()
    tk.Entry(root, textvariable=decrypted_text, width=50).pack()
    
    root.mainloop()

# Hauptprogramm
key = generate_key()
create_gui()
