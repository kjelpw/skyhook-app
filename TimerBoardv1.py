import tkinter as tk
from tkinter import ttk
import time
import json
import os

class TimerBoard:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer Board")
        self.timers = []  # List to store timer data
        
        # Configure root window to expand and fill the entire screen
        root.grid_rowconfigure(0, weight=1, minsize=400)  # Make row 0 resizable
        root.grid_columnconfigure(0, weight=1)  # Make column 0 resizable
        
        # Create a Canvas and Scrollbar for scroll functionality
        canvas = tk.Canvas(root)
        canvas.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')

        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame that will hold the timers
        self.timer_frame = ttk.Frame(canvas, padding=10)
        canvas.create_window((0, 0), window=self.timer_frame, anchor="nw")

        self.timer_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Frame to hold the headers
        header_frame = ttk.Frame(self.timer_frame, padding=10)
        header_frame.grid(row=0, column=0, pady=10, sticky='ew')
        
        # Create headers
        ttk.Label(header_frame, text="System", width=15).grid(row=0, column=0, padx=5)
        ttk.Label(header_frame, text="Planet", width=15).grid(row=0, column=1, padx=5)
        ttk.Label(header_frame, text="Moon", width=15).grid(row=0, column=2, padx=5)
        ttk.Label(header_frame, text="Skyhook", width=15).grid(row=0, column=3, padx=5)
        ttk.Label(header_frame, text="Countdown (DD:HH)", width=20).grid(row=0, column=4, padx=5)
        ttk.Label(header_frame, text="Action", width=10).grid(row=0, column=5, padx=5)

        # Button to add new timers
        ttk.Button(root, text="Add Timer", command=self.add_timer).grid(row=1, column=0, pady=10)

        # Load saved timers if any
        self.load_timers()

        # Set up a protocol to save timers when the application is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_timer(self):
        # Create a frame for each timer
        timer_frame = ttk.Frame(self.timer_frame, padding=10)
        timer_frame.grid(row=len(self.timers) + 1, column=0, pady=5, sticky='ew')

        # Create entries for each timer
        system_entry = ttk.Entry(timer_frame, width=15)
        system_entry.grid(row=0, column=0, padx=5)

        planet_entry = ttk.Entry(timer_frame, width=15)
        planet_entry.grid(row=0, column=1, padx=5)

        moon_entry = ttk.Entry(timer_frame, width=15)
        moon_entry.grid(row=0, column=2, padx=5)

        skyhook_entry = ttk.Entry(timer_frame, width=15)
        skyhook_entry.grid(row=0, column=3, padx=5)

        # Countdown input (Days:Hours)
        countdown_entry = ttk.Entry(timer_frame, width=15)
        countdown_entry.grid(row=0, column=4, padx=5)

        # Timer label to display the countdown
        timer_label = ttk.Label(timer_frame, text="00:00:00", font=("Arial", 14))
        timer_label.grid(row=1, column=0, columnspan=5, pady=5)

        # Add buttons for each timer
        start_button = ttk.Button(timer_frame, text="Start", command=lambda: self.start_timer(timer_label, countdown_entry))
        start_button.grid(row=2, column=0, padx=5)

        stop_button = ttk.Button(timer_frame, text="Stop", command=lambda: self.stop_timer(timer_label))
        stop_button.grid(row=2, column=1, padx=5)

        reset_button = ttk.Button(timer_frame, text="Reset", command=lambda: self.reset_timer(timer_label))
        reset_button.grid(row=2, column=2, padx=5)

        # Delete button to remove the timer
        delete_button = ttk.Button(timer_frame, text="Delete", command=lambda: self.delete_timer(timer_frame))
        delete_button.grid(row=2, column=4, padx=5)

        # Store timer data
        self.timers.append({
            "label": timer_label,
            "system": system_entry,
            "planet": planet_entry,
            "moon": moon_entry,
            "skyhook": skyhook_entry,
            "countdown_time": countdown_entry,
            "start_time": None,
            "running": False,
            "elapsed": 0,
            "target_time": 0,
            "frame": timer_frame
        })

    def start_timer(self, label, countdown_entry):
        for timer in self.timers:
            if timer["label"] == label and not timer["running"]:
                try:
                    countdown_str = countdown_entry.get()
                    days, hours = self.parse_time(countdown_str)
                    if days is None:
                        raise ValueError("Invalid time format. Use DD:HH.")
                    
                    target_time = (days * 86400) + (hours * 3600)  # No minutes or seconds
                except ValueError:
                    return  # Invalid time format input, so just return
                
                timer["target_time"] = target_time
                timer["start_time"] = time.time()
                timer["running"] = True
                self.update_timer(timer)
                break

    def stop_timer(self, label):
        for timer in self.timers:
            if timer["label"] == label and timer["running"]:
                timer["elapsed"] += time.time() - timer["start_time"]
                timer["running"] = False
                break

    def reset_timer(self, label):
        for timer in self.timers:
            if timer["label"] == label:
                timer["start_time"] = None
                timer["running"] = False
                timer["elapsed"] = 0
                timer["target_time"] = 0
                timer["label"].config(text="00:00:00")
                break

    def update_timer(self, timer):
        if timer["running"]:
            elapsed = time.time() - timer["start_time"] + timer["elapsed"]
            remaining_time = timer["target_time"] - elapsed
            if remaining_time <= 0:
                timer["label"].config(text="00:00:00")
                timer["running"] = False
            else:
                timer["label"].config(text=self.format_time(remaining_time))
                self.root.after(1000, lambda: self.update_timer(timer))  # Update every second

    def delete_timer(self, timer_frame):
        """Deletes the timer from the display."""
        for timer in self.timers:
            if timer["frame"] == timer_frame:
                timer["frame"].destroy()
                self.timers.remove(timer)
                break

    def parse_time(self, time_str):
        """Parse time in the format DD:HH"""
        try:
            parts = list(map(int, time_str.split(":")))
            if len(parts) == 2:
                days, hours = parts
                if 0 <= hours < 24:
                    return days, hours
            return None, None
        except ValueError:
            return None, None

    def format_time(self, seconds):
        """Convert total seconds to DD:HH:MM:SS format"""
        days = int(seconds // 86400)
        seconds %= 86400
        hours = int(seconds // 3600)
        seconds %= 3600
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{days:02}:{hours:02}:{minutes:02}:{seconds:02}"

    def save_timers(self):
        """Save the current timers to a file."""
        timers_data = []
        for timer in self.timers:
            timer_data = {
                "system": timer["system"].get(),
                "planet": timer["planet"].get(),
                "moon": timer["moon"].get(),
                "skyhook": timer["skyhook"].get(),
                "countdown_time": timer["countdown_time"].get(),
                "running": timer["running"],
                "elapsed": timer["elapsed"],
                "start_time": timer["start_time"],
                "target_time": timer["target_time"]
            }
            timers_data.append(timer_data)

        with open("timers.json", "w") as file:
            json.dump(timers_data, file)

    def load_timers(self):
        """Load saved timers from a file."""
        if os.path.exists("timers.json"):
            with open("timers.json", "r") as file:
                timers_data = json.load(file)

            for timer_data in timers_data:
                self.add_timer()
                timer = self.timers[-1]
                timer["system"].insert(0, timer_data["system"])
                timer["planet"].insert(0, timer_data["planet"])
                timer["moon"].insert(0, timer_data["moon"])
                timer["skyhook"].insert(0, timer_data["skyhook"])
                timer["countdown_time"].insert(0, timer_data["countdown_time"])
                timer["running"] = timer_data["running"]
                timer["elapsed"] = timer_data["elapsed"]
                timer["start_time"] = timer_data["start_time"]
                timer["target_time"] = timer_data["target_time"]
                
                if timer_data["running"]:
                    self.update_timer(timer)

    def on_close(self):
        """Handle saving data when closing the application."""
        self.save_timers()
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = TimerBoard(root)
    root.mainloop()
