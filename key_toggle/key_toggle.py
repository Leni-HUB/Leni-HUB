import keyboard
import threading
import time
import customtkinter as ctk
from tkinter import messagebox
import json
import os

class KeyDetectEntry(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.value = ""
        
        # Create entry and clear button in a frame
        self.entry = ctk.CTkEntry(
            self,
            width=kwargs.get('width', 200),
            height=kwargs.get('height', 35),
            placeholder_text=kwargs.get('placeholder_text', ''),
            font=kwargs.get('font', ("Arial", 14))
        )
        self.entry.pack(side="left", padx=(0, 5))
        
        # Clear button (X)
        clear_btn = ctk.CTkButton(
            self,
            text="×",
            width=25,
            height=25,
            command=self.clear_entry,
            font=("Arial", 16)
        )
        clear_btn.pack(side="left")
        
        # Bind events
        self.entry.bind('<FocusIn>', self.start_listening)
        self.entry.bind('<FocusOut>', self.stop_listening)
        self.listening = False
        self.hook = None
    
    def start_listening(self, event):
        if not self.listening:
            self.listening = True
            self.hook = keyboard.on_press(self.on_key_press)
            self.entry.configure(text_color="green")
    
    def stop_listening(self, event):
        if self.listening:
            self.listening = False
            if self.hook:
                keyboard.unhook(self.hook)
            self.entry.configure(text_color="white")
    
    def on_key_press(self, event):
        if self.listening:
            self.value = event.name
            self.entry.delete(0, 'end')
            self.entry.insert(0, f"{event.name} [Toggle Key]")
            self.stop_listening(None)
    
    def clear_entry(self):
        self.value = ""
        self.entry.delete(0, 'end')
    
    def get(self):
        return self.value
    
    def set(self, value):
        self.value = value
        self.entry.delete(0, 'end')
        self.entry.insert(0, f"{value} [Toggle Key]")

class Profile:
    def __init__(self, name, trigger_key, toggle_keys, group=None):
        self.name = name
        self.trigger_key = trigger_key
        self.toggle_keys = toggle_keys
        self.group = group

class ProfileTab(ctk.CTkFrame):
    def __init__(self, parent, profile_manager, profile=None):
        super().__init__(parent)
        self.profile_manager = profile_manager
        self.manual_mode = profile_manager.settings.get('manual_mode', False)
        self.create_widgets()
        if profile:
            self.load_profile(profile)
    
    def create_widgets(self):
        # Trigger Key
        trigger_frame = ctk.CTkFrame(self)
        trigger_frame.pack(fill="x", padx=10, pady=5)
        
        trigger_label = ctk.CTkLabel(
            trigger_frame,
            text="Activation Key",
            font=("Arial", 16, "bold")
        )
        trigger_label.pack(pady=5)
        
        self.trigger_key_input = KeyDetectEntry(
            trigger_frame,
            placeholder_text="Click and press a key...",
            width=200,
            height=35,
            font=("Arial", 14)
        )
        self.trigger_key_input.pack(pady=5)
        
        # Toggle Keys Frame
        toggle_frame = ctk.CTkFrame(self)
        toggle_frame.pack(fill="x", padx=10, pady=5)
        
        toggle_label = ctk.CTkLabel(
            toggle_frame,
            text="Toggle Keys",
            font=("Arial", 16, "bold")
        )
        toggle_label.pack(pady=5)
        
        # Add single key input
        self.new_key_input = KeyDetectEntry(
            toggle_frame,
            placeholder_text="Click and press a key to add...",
            width=200,
            height=35,
            font=("Arial", 14)
        )
        self.new_key_input.pack(pady=5)
        
        add_key_button = ctk.CTkButton(
            toggle_frame,
            text="Add Key",
            command=self.add_toggle_key,
            width=100
        )
        add_key_button.pack(pady=5)
        
        # Keys list
        self.keys_listbox = ctk.CTkTextbox(
            toggle_frame,
            height=150,
            width=300,
            font=("Arial", 14)
        )
        self.keys_listbox.pack(pady=5)
        
        # Remove key button
        remove_key_button = ctk.CTkButton(
            toggle_frame,
            text="Remove Selected Key",
            command=self.remove_toggle_key,
            width=150
        )
        remove_key_button.pack(pady=5)
        
        # Group selection if enabled
        if self.profile_manager.settings.get('manual_mode'):
            group_frame = ctk.CTkFrame(self)
            group_frame.pack(fill="x", padx=10, pady=5)
            
            group_label = ctk.CTkLabel(
                group_frame,
                text="Group",
                font=("Arial", 16, "bold")
            )
            group_label.pack(pady=5)
            
            self.group_var = ctk.StringVar(value="none")
            self.group_menu = ctk.CTkOptionMenu(
                group_frame,
                values=["none"] + list(self.profile_manager.settings.get('groups', {}).keys()),
                variable=self.group_var
            )
            self.group_menu.pack(pady=5)
            
            new_group_frame = ctk.CTkFrame(group_frame)
            new_group_frame.pack(fill="x", pady=5)
            
            self.new_group_input = ctk.CTkEntry(
                new_group_frame,
                placeholder_text="New group name...",
                width=150
            )
            self.new_group_input.pack(side="left", padx=5)
            
            add_group_button = ctk.CTkButton(
                new_group_frame,
                text="Add Group",
                command=self.add_group,
                width=100
            )
            add_group_button.pack(side="left", padx=5)
        
        # Manual activation button if enabled
        if self.profile_manager.settings.get('manual_mode'):
            self.toggle_button = ctk.CTkButton(
                self,
                text="Toggle Keys: OFF",
                command=self.manual_toggle,
                width=200,
                height=40,
                font=("Arial", 14, "bold")
            )
            self.toggle_button.pack(pady=10)
        
        # Status
        self.status_label = ctk.CTkLabel(
            self,
            text="Status: Inactive",
            font=("Arial", 14)
        )
        self.status_label.pack(pady=5)
        
        self.active_keys_label = ctk.CTkLabel(
            self,
            text="Active keys: None",
            font=("Arial", 14)
        )
        self.active_keys_label.pack(pady=5)
    
    def add_group(self):
        group_name = self.new_group_input.get().strip()
        if group_name and group_name != "none":
            groups = self.profile_manager.settings.get('groups', {})
            if group_name not in groups:
                groups[group_name] = []
                self.profile_manager.settings['groups'] = groups
                self.profile_manager.save_settings()
                
                # Update group menu
                self.group_menu.configure(values=["none"] + list(groups.keys()))
                self.group_var.set(group_name)
                
                self.new_group_input.delete(0, 'end')
    
    def manual_toggle(self):
        name = self.profile_manager.get_current_tab_name()
        if name:
            self.profile_manager.toggle_profile_keys(name)
            is_active = bool(self.profile_manager.key_toggle.get_active_keys())
            self.toggle_button.configure(
                text=f"Toggle Keys: {'ON' if is_active else 'OFF'}",
                fg_color="green" if is_active else "gray"
            )
    
    def add_toggle_key(self):
        key = self.new_key_input.get().strip()
        if key:
            current_keys = self.get_toggle_keys()
            if key not in current_keys:
                self.keys_listbox.insert("end", f"{key} [Toggle]\n")
            self.new_key_input.clear_entry()
    
    def remove_toggle_key(self):
        try:
            sel_start = self.keys_listbox.index("sel.first")
            sel_end = self.keys_listbox.index("sel.last")
            self.keys_listbox.delete(sel_start, sel_end)
        except:
            messagebox.showwarning("Error", "Please select a key to remove")
    
    def get_toggle_keys(self):
        return [k.split(" [")[0].strip() for k in self.keys_listbox.get("1.0", "end").split('\n') if k.strip()]
    
    def get_group(self):
        if hasattr(self, 'group_var'):
            group = self.group_var.get()
            return group if group != "none" else None
        return None
    
    def load_profile(self, profile):
        self.trigger_key_input.set(profile.trigger_key)
        
        self.keys_listbox.delete("1.0", "end")
        for key in profile.toggle_keys:
            self.keys_listbox.insert("end", f"{key} [Toggle]\n")
        
        if hasattr(self, 'group_var') and profile.group:
            self.group_var.set(profile.group)
    
    def update_status(self, active_keys):
        if active_keys:
            self.status_label.configure(text="Status: Active")
            self.active_keys_label.configure(text=f"Active keys: {', '.join(active_keys)}")
            if hasattr(self, 'toggle_button'):
                self.toggle_button.configure(text="Toggle Keys: ON", fg_color="green")
        else:
            self.status_label.configure(text="Status: Inactive")
            self.active_keys_label.configure(text="Active keys: None")
            if hasattr(self, 'toggle_button'):
                self.toggle_button.configure(text="Toggle Keys: OFF", fg_color="gray")

class FirstRunDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Welcome to Key Toggle Pro!")
        self.geometry("400x300")
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Center on parent
        x = parent.winfo_x() + (parent.winfo_width() / 2) - (400 / 2)
        y = parent.winfo_y() + (parent.winfo_height() / 2) - (300 / 2)
        self.geometry(f"+{int(x)}+{int(y)}")
        
        self.result = None
        self.create_widgets()
    
    def create_widgets(self):
        title = ctk.CTkLabel(
            self,
            text="Welcome to Key Toggle Pro!",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=20)
        
        msg = ctk.CTkLabel(
            self,
            text="How would you like to use the program?",
            font=("Arial", 14)
        )
        msg.pack(pady=10)
        
        # Auto mode button
        auto_btn = ctk.CTkButton(
            self,
            text="Automatic Mode",
            command=lambda: self.choose_mode(False),
            width=200,
            height=40
        )
        auto_btn.pack(pady=10)
        
        auto_desc = ctk.CTkLabel(
            self,
            text="Keys toggle automatically when pressing\nthe activation key",
            font=("Arial", 12)
        )
        auto_desc.pack()
        
        # Manual mode button
        manual_btn = ctk.CTkButton(
            self,
            text="Manual Mode",
            command=lambda: self.choose_mode(True),
            width=200,
            height=40
        )
        manual_btn.pack(pady=10)
        
        manual_desc = ctk.CTkLabel(
            self,
            text="Use buttons to toggle keys and\norganize them in groups",
            font=("Arial", 12)
        )
        manual_desc.pack()
    
    def choose_mode(self, manual):
        self.result = manual
        self.destroy()

class KeyToggleGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Load settings
        self.settings = self.load_settings()
        
        # Show first run dialog if needed
        if self.settings.get('first_run', True):
            self.show_first_run_dialog()
        
        # Configure window
        self.title("Key Toggle Pro - Profile Edition")
        self.geometry("1000x700")
        ctk.set_appearance_mode("dark")
        
        # Initialize key toggle system
        self.key_toggle = KeyToggle()
        self.profiles = {}
        self.tabs = {}
        
        # Load profiles
        self.load_profiles()
        
        # Create GUI elements
        self.create_widgets()
        
        # Window close handler
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def show_first_run_dialog(self):
        dialog = FirstRunDialog(self)
        self.wait_window(dialog)
        
        self.settings['manual_mode'] = dialog.result
        self.settings['first_run'] = False
        self.save_settings()
    
    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {'manual_mode': False, 'first_run': True, 'groups': {}}
    
    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f, indent=4)
    
    def load_profiles(self):
        try:
            with open('profiles.json', 'r') as f:
                data = json.load(f)
                for name, profile_data in data['profiles'].items():
                    self.profiles[name] = Profile(
                        name,
                        profile_data['trigger_key'],
                        profile_data['toggle_keys'],
                        profile_data.get('group')
                    )
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_profiles()
    
    def save_profiles(self):
        data = {
            'profiles': {
                name: {
                    'trigger_key': profile.trigger_key,
                    'toggle_keys': profile.toggle_keys,
                    'group': profile.group
                }
                for name, profile in self.profiles.items()
            }
        }
        with open('profiles.json', 'w') as f:
            json.dump(data, f, indent=4)
    
    def create_widgets(self):
        # Main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Top bar with profile management
        top_frame = ctk.CTkFrame(self)
        top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        # Profile name input
        self.profile_name = ctk.CTkEntry(
            top_frame,
            placeholder_text="Profile name...",
            width=200
        )
        self.profile_name.pack(side="left", padx=5)
        
        # Profile buttons
        new_button = ctk.CTkButton(
            top_frame,
            text="New Profile",
            command=self.new_profile,
            width=100
        )
        new_button.pack(side="left", padx=5)
        
        save_button = ctk.CTkButton(
            top_frame,
            text="Save Profile",
            command=self.save_profile,
            width=100
        )
        save_button.pack(side="left", padx=5)
        
        delete_button = ctk.CTkButton(
            top_frame,
            text="Delete Profile",
            command=self.delete_profile,
            width=100
        )
        delete_button.pack(side="left", padx=5)
        
        # Tabs container
        self.tab_container = ctk.CTkTabview(self)
        self.tab_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        # Load existing profiles as tabs
        for name, profile in self.profiles.items():
            self.add_profile_tab(name, profile)
    
    def get_current_tab_name(self):
        return self.tab_container.get()
    
    def add_profile_tab(self, name, profile=None):
        tab = self.tab_container.add(name)
        profile_tab = ProfileTab(tab, self, profile)
        profile_tab.pack(fill="both", expand=True)
        self.tabs[name] = profile_tab
        return profile_tab
    
    def new_profile(self):
        name = self.profile_name.get().strip()
        if not name:
            messagebox.showwarning("Error", "Please enter a profile name!")
            return
        
        if name in self.tabs:
            messagebox.showwarning("Error", "Profile already exists!")
            return
        
        self.add_profile_tab(name)
        self.tab_container.set(name)
    
    def save_profile(self):
        name = self.profile_name.get().strip()
        if not name:
            messagebox.showwarning("Error", "Please enter a profile name!")
            return
        
        if name not in self.tabs:
            messagebox.showwarning("Error", "Profile not found! Create it first.")
            return
        
        tab = self.tabs[name]
        trigger_key = tab.trigger_key_input.get().strip()
        toggle_keys = tab.get_toggle_keys()
        group = tab.get_group()
        
        if not trigger_key or not toggle_keys:
            messagebox.showwarning("Error", "Please set both trigger key and toggle keys!")
            return
        
        # Remove old key binding if exists
        if name in self.profiles:
            keyboard.unhook_all()
        
        # Save profile
        self.profiles[name] = Profile(name, trigger_key, toggle_keys, group)
        self.save_profiles()
        
        # Set up key binding if not in manual mode
        if not self.settings.get('manual_mode'):
            keyboard.on_press_key(trigger_key, lambda _: self.toggle_profile_keys(name))
        
        messagebox.showinfo("Success", f"Profile '{name}' saved!")
    
    def delete_profile(self):
        name = self.profile_name.get().strip()
        if not name:
            messagebox.showwarning("Error", "Please enter a profile name!")
            return
        
        if name not in self.profiles:
            messagebox.showwarning("Error", "Profile not found!")
            return
        
        if messagebox.askyesno("Confirm Delete", f"Delete profile '{name}'?"):
            # Remove key bindings
            keyboard.unhook_all()
            
            # Remove profile
            del self.profiles[name]
            self.save_profiles()
            
            # Remove tab
            self.tab_container.delete(name)
            del self.tabs[name]
            
            messagebox.showinfo("Success", f"Profile '{name}' deleted!")
    
    def toggle_profile_keys(self, profile_name):
        if profile_name not in self.profiles:
            return
        
        profile = self.profiles[profile_name]
        
        # If in manual mode and profile is in a group, toggle all profiles in that group
        if self.settings.get('manual_mode') and profile.group:
            keys_to_toggle = []
            for p in self.profiles.values():
                if p.group == profile.group:
                    keys_to_toggle.extend(p.toggle_keys)
            active = self.key_toggle.toggle_keys(keys_to_toggle)
        else:
            active = self.key_toggle.toggle_keys(profile.toggle_keys)
        
        # Update status in tab
        self.tabs[profile_name].update_status(
            self.key_toggle.get_active_keys() if active else []
        )
    
    def on_closing(self):
        self.key_toggle.stop()
        self.destroy()

class KeyToggle:
    def __init__(self):
        self.toggled_keys = set()
        self.running = True
        self.hold_thread = threading.Thread(target=self._hold_keys)
        self.hold_thread.daemon = True
        self.hold_thread.start()

    def toggle_keys(self, keys):
        if self.toggled_keys:
            for key in self.toggled_keys:
                keyboard.release(key)
            self.toggled_keys.clear()
            return False
        else:
            self.toggled_keys.update(keys)
            return True

    def get_active_keys(self):
        return list(self.toggled_keys)

    def clear_all(self):
        for key in self.toggled_keys:
            keyboard.release(key)
        self.toggled_keys.clear()

    def _hold_keys(self):
        while self.running:
            for key in self.toggled_keys:
                keyboard.press(key)
            time.sleep(0.1)

    def stop(self):
        self.running = False
        self.clear_all()

if __name__ == "__main__":
    app = KeyToggleGUI()
    app.mainloop()
