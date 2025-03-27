import tkinter as tk
from tkinter import ttk

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.geometry("400x600")
        self.root.configure(bg='#2b2b2b')
        
        # Variables
        self.time_left = tk.StringVar(value="00:00")
        self.is_running = False
        self.timer = None
        self.custom_timers = []
        
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        style = ttk.Style()
        style.configure(
            'Timer.TButton',
            background='white',
            foreground='black',
            font=('Segoe UI', 11),
            padding=10
        )
        
        style.configure(
            'Add.TButton',
            background='white',
            foreground='black',
            font=('Segoe UI', 11),
            padding=10
        )
        
        style.configure(
            'Title.TLabel',
            background='#2b2b2b',
            foreground='white',
            font=('Segoe UI', 12)
        )
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Timer display
        self.time_label = tk.Label(
            main_frame,
            textvariable=self.time_left,
            font=('Segoe UI', 72),
            bg='#2b2b2b',
            fg='white'
        )
        self.time_label.pack(pady=(20, 30))
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Preset timers section
        ttk.Label(
            main_frame,
            text="Voreingestellte Timer",
            style='Title.TLabel'
        ).pack(pady=10)
        
        # Preset buttons frame
        preset_frame = tk.Frame(main_frame, bg='#2b2b2b')
        preset_frame.pack(fill='x')
        
        # First row of presets
        row1 = tk.Frame(preset_frame, bg='#2b2b2b')
        row1.pack(fill='x', pady=5)
        
        ttk.Button(
            row1,
            text="10 Minuten",
            style='Timer.TButton',
            command=lambda: self.set_time(600)
        ).pack(side='left', expand=True, padx=2, fill='x')
        
        ttk.Button(
            row1,
            text="15 Minuten",
            style='Timer.TButton',
            command=lambda: self.set_time(900)
        ).pack(side='left', expand=True, padx=2, fill='x')
        
        # Second row of presets
        row2 = tk.Frame(preset_frame, bg='#2b2b2b')
        row2.pack(fill='x', pady=5)
        
        ttk.Button(
            row2,
            text="60 Sekunden",
            style='Timer.TButton',
            command=lambda: self.set_time(60)
        ).pack(side='left', expand=True, padx=2, fill='x')
        
        ttk.Button(
            row2,
            text="120 Sekunden",
            style='Timer.TButton',
            command=lambda: self.set_time(120)
        ).pack(side='left', expand=True, padx=2, fill='x')
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=20)
        
        # Custom timer section
        ttk.Label(
            main_frame,
            text="Eigenen Timer erstellen",
            style='Title.TLabel'
        ).pack(pady=10)
        
        # Time input frame
        time_frame = tk.Frame(main_frame, bg='#2b2b2b')
        time_frame.pack(fill='x', pady=5)
        
        # Minutes entry
        self.minutes_entry = ttk.Entry(time_frame, width=3, justify='center')
        self.minutes_entry.insert(0, "0")
        self.minutes_entry.pack(side='left', padx=2)
        
        tk.Label(
            time_frame,
            text="min",
            bg='#2b2b2b',
            fg='white',
            font=('Segoe UI', 10)
        ).pack(side='left', padx=(0, 10))
        
        # Seconds entry
        self.seconds_entry = ttk.Entry(time_frame, width=3, justify='center')
        self.seconds_entry.insert(0, "0")
        self.seconds_entry.pack(side='left', padx=2)
        
        tk.Label(
            time_frame,
            text="sec",
            bg='#2b2b2b',
            fg='white',
            font=('Segoe UI', 10)
        ).pack(side='left')
        
        # Label entry
        self.label_entry = ttk.Entry(main_frame)
        self.label_entry.insert(0, "Bezeichnung")
        self.label_entry.pack(fill='x', pady=10)
        
        # Add timer button
        ttk.Button(
            main_frame,
            text="Timer hinzufügen",
            style='Add.TButton',
            command=self.add_custom_timer
        ).pack(fill='x', pady=5)
        
        # Custom timers list
        self.custom_list_frame = tk.Frame(main_frame, bg='#2b2b2b')
        self.custom_list_frame.pack(fill='both', expand=True)
        
    def set_time(self, seconds):
        if self.is_running:
            self.stop_timer()
        self.remaining = seconds
        mins, secs = divmod(seconds, 60)
        self.time_left.set(f"{mins:02d}:{secs:02d}")
        self.minutes_entry.delete(0, tk.END)
        self.minutes_entry.insert(0, str(mins))
        self.seconds_entry.delete(0, tk.END)
        self.seconds_entry.insert(0, str(secs))
        
    def add_custom_timer(self):
        try:
            mins = int(self.minutes_entry.get())
            secs = int(self.seconds_entry.get())
            label = self.label_entry.get()
            total_seconds = mins * 60 + secs
            
            if total_seconds > 0:
                btn = ttk.Button(
                    self.custom_list_frame,
                    text=f"{label} ({mins:02d}:{secs:02d})",
                    style='Timer.TButton',
                    command=lambda: self.set_time(total_seconds)
                )
                btn.pack(fill='x', pady=2)
                self.custom_timers.append(btn)
                
                # Reset entries
                self.minutes_entry.delete(0, tk.END)
                self.minutes_entry.insert(0, "0")
                self.seconds_entry.delete(0, tk.END)
                self.seconds_entry.insert(0, "0")
                self.label_entry.delete(0, tk.END)
                self.label_entry.insert(0, "Bezeichnung")
        except ValueError:
            pass
            
    def start_timer(self):
        try:
            mins = int(self.minutes_entry.get())
            secs = int(self.seconds_entry.get())
            total_seconds = mins * 60 + secs
            
            if total_seconds > 0:
                self.remaining = total_seconds
                self.is_running = True
                self.countdown()
        except ValueError:
            pass
            
    def stop_timer(self):
        self.is_running = False
        if self.timer:
            self.root.after_cancel(self.timer)
            
    def countdown(self):
        if self.is_running and self.remaining > 0:
            mins, secs = divmod(self.remaining, 60)
            self.time_left.set(f"{mins:02d}:{secs:02d}")
            self.remaining -= 1
            self.timer = self.root.after(1000, self.countdown)
        elif self.remaining <= 0:
            self.time_left.set("00:00")
            self.stop_timer()
            self.show_times_up()
            
    def show_times_up(self):
        popup = tk.Toplevel(self.root)
        popup.title("Zeit abgelaufen!")
        popup.geometry("300x150")
        popup.configure(bg='#2b2b2b')
        
        tk.Label(
            popup,
            text="Zeit ist abgelaufen!",
            bg='#2b2b2b',
            fg='white',
            font=('Segoe UI', 14)
        ).pack(expand=True)
        
        ttk.Button(
            popup,
            text="OK",
            style='Timer.TButton',
            command=popup.destroy
        ).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()
