import tkinter as tk
from tkinter import Variable, ttk
import csv
import os
import TKinterModernThemes as TKMT

CSV_FILE = 'data.csv'
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 250
WINDOW_X = 100 # Initial X position
WINDOW_Y = 100 # Initial Y position

def load_csv(filepath):
    """Loads data from a CSV file."""
    data = []
    if not os.path.exists(filepath):
        print(f"Error: CSV file not found at {filepath}")
        return data # Return empty list if file not found

    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Optionally skip header row if your CSV has one
            # next(reader)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f"Error loading CSV file: {e}")
    return data

# Load data when the script starts
csv_data = load_csv(CSV_FILE)

# --- GUI Functions ---
def search_data(query, data):
    """Searches the loaded data for rows containing the query."""
    if not query:
        return [] # Return empty list if query is empty
    query = query.lower()
    results = []
    for row in data:
        # Check if the query is in any cell of the row (case-insensitive)
        if any(query in str(cell).lower() for cell in row):
            results.append(row)
    return results

def update_results(event=None):
    """Updates the results listbox based on the search entry."""
    query = search_entry.get()
    matches = search_data(query, csv_data)

    # Clear current results
    results_listbox.delete(0, tk.END)

    # Display new results
    if matches:
        for match in matches:
            # Join the row elements into a single string for display
            results_listbox.insert(tk.END, ", ".join(match))
    else:
        if query:
            results_listbox.insert(tk.END, "No matches found.")
        else:
            results_listbox.insert(tk.END, "Type to search...")

# # Search Entry Field
# search_entry = tk.Entry(root, width=40)
# search_entry.pack(pady=10, padx=10, fill=tk.X)
# search_entry.focus_set() # Set focus to the entry field on startup

# # Bind the update_results function to key releases in the entry field
# search_entry.bind('<KeyRelease>', update_results)

# # Results Listbox with Scrollbar
# results_frame = tk.Frame(root)
# results_frame.pack(pady=0, padx=10, fill=tk.BOTH, expand=True)

# results_scrollbar = tk.Scrollbar(results_frame)
# results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# results_listbox = tk.Listbox(results_frame, yscrollcommand=results_scrollbar.set)
# results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# results_scrollbar.config(command=results_listbox.yview)

# # Initial prompt in the listbox
# results_listbox.insert(tk.END, "Type to search...")

# # Close Button
# close_button = tk.Button(root, text="Close", command=close_window)
# close_button.pack(pady=5)

# # Run the application
# root.mainloop()


class App(TKMT.ThemedTKinterFrame):
    
    def __init__(self):
        super().__init__("Missing Barcodes", "azure", "light")
        self.query = Variable()    
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{WINDOW_X}+{WINDOW_Y}")
        self.root.bind('<ButtonPress-1>', self.window_move_start)
        self.root.bind('<B1-Motion>', self.window_on_move)
        
        self.outer_frame = self.addLabelFrame("Missing Item Barcodes")
        self.outer_frame.Entry(self.query)
        exitButton = self.outer_frame.Button("Close", self.root.destroy)
        
        self.run()
        
    def window_move_start(self, event):
        """Records the starting position for window dragging."""
        self.move_start_x = event.x
        self.move_start_y = event.y

    def window_on_move(self, event):
        """Updates the window position while dragging."""
        x = self.root.winfo_x() + (event.x - self.move_start_x)
        y = self.root.winfo_y() + (event.y - self.move_start_y)
        self.root.geometry(f"+{x}+{y}")


App()
