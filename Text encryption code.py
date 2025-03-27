# -*- coding: utf-8 -*-
"""
Verschlüsselungs-Tool mit mehreren Verschlüsselungsmethoden
Entwickelt im Microsoft Fluent Design Style

Unterstützte Verschlüsselungsmethoden:
- Caesar-Verschlüsselung: Einfache Buchstabenverschiebung
- Vigenère-Verschlüsselung: Polyalphabetische Substitution mit Schlüsselwort
- Rail Fence: Transpositionsverschlüsselung mit variabler Schienenzahl

Author: [Leni]
Version: 1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

class CipherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Verschlüsselungs-Tool")
        self.root.geometry("800x700")  # Vergrößertes Fenster
        self.root.resizable(False, False)
        
        # Microsoft Fluent Design Style
        self.configure_styles()
        
        # Hauptcontainer
        main_container = ttk.Frame(root, padding="10")
        main_container.pack(fill='both', expand=True)
        
        # Info-Panel (Links)
        info_frame = ttk.LabelFrame(main_container, text="Information", padding="10")
        info_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Informationstext
        info_text = """
Verschlüsselungsmethoden:

Caesar:
- Verschiebt jeden Buchstaben
- Einfach und klassisch
- Schlüssel: 0-25

Vigenère:
- Verwendet Schlüsselwort
- Sicherer als Caesar
- Polyalphabetisch

Rail Fence:
- Schreibt Text zickzack
- Geometrische Methode
- 2-10 Schienen
        """
        info_label = ttk.Label(info_frame, text=info_text, justify='left', wraplength=200)
        info_label.pack(fill='x', expand=True)
        
        # Hilfe-Button
        ttk.Button(info_frame, text="Online Hilfe", 
                  command=lambda: webbrowser.open('https://de.wikipedia.org/wiki/Klassische_Verschl%C3%BCsselung')
                  ).pack(side='bottom', pady=10)
        
        # Notebook-Container (Rechts)
        notebook_container = ttk.Frame(main_container)
        notebook_container.pack(side='left', fill='both', expand=True)
        
        # Notebook (Reiter) erstellen
        self.notebook = ttk.Notebook(notebook_container)
        self.notebook.pack(fill='both', expand=True)
        
        # Reiter für verschiedene Verschlüsselungsmethoden
        self.caesar_frame = ttk.Frame(self.notebook, padding=10)
        self.vigenere_frame = ttk.Frame(self.notebook, padding=10)
        self.rail_fence_frame = ttk.Frame(self.notebook, padding=10)
        
        self.notebook.add(self.caesar_frame, text='Caesar')
        self.notebook.add(self.vigenere_frame, text='Vigenère')
        self.notebook.add(self.rail_fence_frame, text='Rail Fence')
        
        # Initialisiere die Reiter
        self.setup_caesar_tab()
        self.setup_vigenere_tab()
        self.setup_rail_fence_tab()
        
        # Status-Bar am unteren Rand
        self.status_var = tk.StringVar()
        self.status_var.set("Bereit")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief='sunken', padding=(5, 2))
        status_bar.pack(side='bottom', fill='x')
        
        # Beenden-Button
        quit_frame = ttk.Frame(root, padding="10")
        quit_frame.pack(fill='x', side='bottom')
        ttk.Button(quit_frame, text="Beenden", command=self.quit_app, style='Accent.TButton').pack(side='right')
    
    def configure_styles(self):
        """Konfiguriert den Microsoft Fluent Design Style"""
        style = ttk.Style()
        
        # Grundlegende Styles
        style.configure('TButton', padding=8)
        style.configure('TLabel', padding=5)
        style.configure('TEntry', padding=5)
        style.configure('TNotebook.Tab', padding=(15, 5))
        style.configure('TLabelframe', padding=10)
        
        # Accent Button Style
        style.configure('Accent.TButton',
                       padding=8,
                       background='#0078D7',  # Microsoft Blue
                       foreground='white')
        
        # Hover-Effekte
        style.map('TButton',
                 background=[('active', '#E5F1FB')],
                 foreground=[('active', '#000000')])
        
        style.map('Accent.TButton',
                 background=[('active', '#106EBE')],
                 foreground=[('active', 'white')])
    
    def setup_caesar_tab(self):
        # Eingabebereich
        ttk.Label(self.caesar_frame, text="Text eingeben:", font=('Arial', 12)).grid(row=0, column=0, sticky=tk.W)
        self.caesar_input = ttk.Entry(self.caesar_frame, width=50)
        self.caesar_input.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Verschiebungswert
        ttk.Label(self.caesar_frame, text="Verschiebungswert (0-25):", font=('Arial', 12)).grid(row=2, column=0, sticky=tk.W)
        self.caesar_shift = ttk.Spinbox(self.caesar_frame, from_=0, to=25, width=5)
        self.caesar_shift.grid(row=2, column=1, sticky=tk.W, pady=5)
        self.caesar_shift.set(3)
        
        # Buttons
        button_frame = ttk.Frame(self.caesar_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Verschlüsseln", command=lambda: self.encrypt('caesar')).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Entschlüsseln", command=lambda: self.decrypt('caesar')).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Alle Möglichkeiten", command=lambda: self.show_all('caesar')).grid(row=0, column=2, padx=5)
        
        # Ergebnisbereich
        ttk.Label(self.caesar_frame, text="Ergebnis:", font=('Arial', 12)).grid(row=4, column=0, sticky=tk.W, pady=(10,0))
        self.caesar_result = tk.Text(self.caesar_frame, height=12, width=60, wrap=tk.WORD)
        self.caesar_result.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Scrollbar
        caesar_scrollbar = ttk.Scrollbar(self.caesar_frame, orient=tk.VERTICAL, command=self.caesar_result.yview)
        caesar_scrollbar.grid(row=5, column=2, sticky=(tk.N, tk.S))
        self.caesar_result.configure(yscrollcommand=caesar_scrollbar.set)
    
    def setup_vigenere_tab(self):
        # Eingabebereich
        ttk.Label(self.vigenere_frame, text="Text eingeben:", font=('Arial', 12)).grid(row=0, column=0, sticky=tk.W)
        self.vigenere_input = ttk.Entry(self.vigenere_frame, width=50)
        self.vigenere_input.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Schlüsselwort
        ttk.Label(self.vigenere_frame, text="Schlüsselwort:", font=('Arial', 12)).grid(row=2, column=0, sticky=tk.W)
        self.vigenere_key = ttk.Entry(self.vigenere_frame, width=20)
        self.vigenere_key.grid(row=2, column=1, sticky=tk.W, pady=5)
        self.vigenere_key.insert(0, "GEHEIM")
        
        # Buttons
        button_frame = ttk.Frame(self.vigenere_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Verschlüsseln", command=lambda: self.encrypt('vigenere')).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Entschlüsseln", command=lambda: self.decrypt('vigenere')).grid(row=0, column=1, padx=5)
        
        # Ergebnisbereich
        ttk.Label(self.vigenere_frame, text="Ergebnis:", font=('Arial', 12)).grid(row=4, column=0, sticky=tk.W, pady=(10,0))
        self.vigenere_result = tk.Text(self.vigenere_frame, height=12, width=60, wrap=tk.WORD)
        self.vigenere_result.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Scrollbar
        vigenere_scrollbar = ttk.Scrollbar(self.vigenere_frame, orient=tk.VERTICAL, command=self.vigenere_result.yview)
        vigenere_scrollbar.grid(row=5, column=2, sticky=(tk.N, tk.S))
        self.vigenere_result.configure(yscrollcommand=vigenere_scrollbar.set)
    
    def setup_rail_fence_tab(self):
        # Eingabebereich
        ttk.Label(self.rail_fence_frame, text="Text eingeben:", font=('Arial', 12)).grid(row=0, column=0, sticky=tk.W)
        self.rail_fence_input = ttk.Entry(self.rail_fence_frame, width=50)
        self.rail_fence_input.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Anzahl der Schienen
        ttk.Label(self.rail_fence_frame, text="Anzahl der Schienen:", font=('Arial', 12)).grid(row=2, column=0, sticky=tk.W)
        self.rail_fence_rails = ttk.Spinbox(self.rail_fence_frame, from_=2, to=10, width=5)
        self.rail_fence_rails.grid(row=2, column=1, sticky=tk.W, pady=5)
        self.rail_fence_rails.set(3)
        
        # Buttons
        button_frame = ttk.Frame(self.rail_fence_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Verschlüsseln", command=lambda: self.encrypt('rail_fence')).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Entschlüsseln", command=lambda: self.decrypt('rail_fence')).grid(row=0, column=1, padx=5)
        
        # Ergebnisbereich
        ttk.Label(self.rail_fence_frame, text="Ergebnis:", font=('Arial', 12)).grid(row=4, column=0, sticky=tk.W, pady=(10,0))
        self.rail_fence_result = tk.Text(self.rail_fence_frame, height=12, width=60, wrap=tk.WORD)
        self.rail_fence_result.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Scrollbar
        rail_fence_scrollbar = ttk.Scrollbar(self.rail_fence_frame, orient=tk.VERTICAL, command=self.rail_fence_result.yview)
        rail_fence_scrollbar.grid(row=5, column=2, sticky=(tk.N, tk.S))
        self.rail_fence_result.configure(yscrollcommand=rail_fence_scrollbar.set)
    
    def caesar_cipher(self, text, shift):
        """Caesar-Verschlüsselung"""
        umlaut_map = {
            'ä': 'ae', 'ö': 'oe', 'ü': 'ue',
            'Ä': 'AE', 'Ö': 'OE', 'Ü': 'UE',
            'ß': 'ss'
        }
        
        for umlaut, replacement in umlaut_map.items():
            text = text.replace(umlaut, replacement)
        
        result = ""
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shifted_char = chr((ord(char) - base + shift) % 26 + base)
                result += shifted_char
            else:
                result += char
        return result
    
    def vigenere_cipher(self, text, key, decrypt=False):
        """Vigenère-Verschlüsselung"""
        umlaut_map = {
            'ä': 'ae', 'ö': 'oe', 'ü': 'ue',
            'Ä': 'AE', 'Ö': 'OE', 'Ü': 'UE',
            'ß': 'ss'
        }
        
        for umlaut, replacement in umlaut_map.items():
            text = text.replace(umlaut, replacement)
        
        key = key.upper()
        if not key.isalpha():
            raise ValueError("Schlüssel darf nur Buchstaben enthalten")
        
        result = ""
        key_idx = 0
        
        for char in text:
            if char.isalpha():
                # Bestimme die Basis (A oder a)
                base = ord('A') if char.isupper() else ord('a')
                # Berechne Verschiebung
                key_shift = ord(key[key_idx % len(key)]) - ord('A')
                if decrypt:
                    key_shift = -key_shift
                # Verschiebe den Buchstaben
                char_idx = ord(char) - base
                shifted_idx = (char_idx + key_shift) % 26
                result += chr(shifted_idx + base)
                key_idx += 1
            else:
                result += char
        return result
    
    def rail_fence_cipher(self, text, rails, decrypt=False):
        """Rail Fence Verschlüsselung"""
        if not 2 <= rails <= 10:
            raise ValueError("Anzahl der Schienen muss zwischen 2 und 10 liegen")
        
        if decrypt:
            return self._rail_fence_decrypt(text, rails)
        return self._rail_fence_encrypt(text, rails)
    
    def _rail_fence_encrypt(self, text, rails):
        """Hilfsfunktion für Rail Fence Verschlüsselung"""
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1
        
        for char in text:
            fence[rail].append(char)
            rail += direction
            if rail == rails - 1 or rail == 0:
                direction = -direction
        
        return ''.join([''.join(rail) for rail in fence])
    
    def _rail_fence_decrypt(self, text, rails):
        """Hilfsfunktion für Rail Fence Entschlüsselung"""
        fence = [[] for _ in range(rails)]
        length = len(text)
        
        # Berechne die Positionen
        positions = []
        rail = 0
        direction = 1
        for i in range(length):
            positions.append(rail)
            rail += direction
            if rail == rails - 1 or rail == 0:
                direction = -direction
        
        # Verteile die Buchstaben
        index = 0
        for rail in range(rails):
            for pos in range(length):
                if positions[pos] == rail:
                    fence[rail].append(text[index])
                    index += 1
        
        # Lies die Nachricht
        result = ''
        rail = 0
        direction = 1
        for _ in range(length):
            result += fence[rail].pop(0)
            rail += direction
            if rail == rails - 1 or rail == 0:
                direction = -direction
        
        return result
    
    def get_input_and_validate(self, cipher_type):
        """Holt und validiert die Eingaben je nach Verschlüsselungstyp"""
        if cipher_type == 'caesar':
            text = self.caesar_input.get().strip()
            try:
                shift = int(self.caesar_shift.get())
                if not (0 <= shift <= 25):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Fehler", "Bitte geben Sie eine Zahl zwischen 0 und 25 ein!")
                return None, None
        elif cipher_type == 'vigenere':
            text = self.vigenere_input.get().strip()
            key = self.vigenere_key.get().strip()
            if not key:
                messagebox.showerror("Fehler", "Bitte geben Sie ein Schlüsselwort ein!")
                return None, None
            shift = key
        elif cipher_type == 'rail_fence':
            text = self.rail_fence_input.get().strip()
            try:
                shift = int(self.rail_fence_rails.get())
                if not (2 <= shift <= 10):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Fehler", "Bitte geben Sie eine Zahl zwischen 2 und 10 ein!")
                return None, None
        
        if not text:
            messagebox.showerror("Fehler", "Bitte geben Sie einen Text ein!")
            return None, None
        
        return text, shift
    
    def show_result(self, cipher_type, text):
        """Zeigt das Ergebnis im entsprechenden Textfeld an"""
        result_widget = getattr(self, f"{cipher_type}_result")
        result_widget.delete(1.0, tk.END)
        result_widget.insert(tk.END, text)
    
    def encrypt(self, cipher_type):
        """Verschlüsselt den Text mit der gewählten Methode"""
        text, shift = self.get_input_and_validate(cipher_type)
        if text is None or shift is None:
            return
        
        try:
            if cipher_type == 'caesar':
                result = self.caesar_cipher(text, shift)
            elif cipher_type == 'vigenere':
                result = self.vigenere_cipher(text, shift)
            else:  # rail_fence
                result = self.rail_fence_cipher(text, shift)
            
            self.show_result(cipher_type, f"Verschlüsselter Text:\n{result}")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
    
    def decrypt(self, cipher_type):
        """Entschlüsselt den Text mit der gewählten Methode"""
        text, shift = self.get_input_and_validate(cipher_type)
        if text is None or shift is None:
            return
        
        try:
            if cipher_type == 'caesar':
                result = self.caesar_cipher(text, -shift)
            elif cipher_type == 'vigenere':
                result = self.vigenere_cipher(text, shift, decrypt=True)
            else:  # rail_fence
                result = self.rail_fence_cipher(text, shift, decrypt=True)
            
            self.show_result(cipher_type, f"Entschlüsselter Text:\n{result}")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
    
    def show_all(self, cipher_type):
        """Zeigt alle möglichen Caesar-Verschiebungen an"""
        if cipher_type != 'caesar':
            return
        
        text = self.caesar_input.get().strip()
        if not text:
            messagebox.showerror("Fehler", "Bitte geben Sie einen Text ein!")
            return
        
        results = []
        for shift in range(26):
            decrypted = self.caesar_cipher(text, -shift)
            results.append(f"Verschiebung {shift:2d}: {decrypted}")
        
        self.show_result('caesar', "Alle möglichen Entschlüsselungen:\n" + "\n".join(results))
    
    def quit_app(self):
        self.root.destroy()

def main():
    root = tk.Tk()
    app = CipherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
