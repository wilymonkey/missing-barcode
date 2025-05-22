import tkinter as tk
from tkinter import StringVar, Variable, ttk
import csv
import os
import TKinterModernThemes as TKMT
from typing import Tuple

CSV_FILE = 'data.csv'
WINDOW_WIDTH = 200
WINDOW_HEIGHT = 250
WINDOW_X = 100 # Initial X position
WINDOW_Y = 100 # Initial Y position

def load_data(filepath) -> Tuple[list[str], list[list[str]]]:
    """Loads data from a CSV file."""
    headers = []
    data = []    
    
    if not os.path.exists(filepath):
        print(f"Error: CSV file not found at {filepath}")
        return (headers, data)
    
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)
            data = [row for row in reader]
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        
    return (headers, data)

def search_data(query: str, data: list[list[str]]) -> list[list[str]]:
    """Searches the loaded data for rows containing the query."""
    
    if not query:
        return [] 
    
    query = query.lower()
    results = []
    
    for row in data:
        if query in row[0].lower():
            results.append(row)
    return results

class App(TKMT.ThemedTKinterFrame):
    headers, data = load_data(CSV_FILE)
    
    def __init__(self):
        super().__init__("Missing Barcodes", "azure", "light")
        self.root.attributes('-topmost', True)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{WINDOW_X}+{WINDOW_Y}")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.main_frame = self.addFrame('main_frame', sticky='nsew', padx=5, pady=5)
        
        self.query = StringVar()
        search_box = self.main_frame.Entry(self.query, row=0, col=0)
        search_box.bind('<KeyRelease>', self.update_results)
        search_box.focus_set() # Set focus on startup
                        
        self.results_frame = self.main_frame.addLabelFrame("Items", sticky='nsew')
        self.results_frame.master.grid_columnconfigure(0, weight=1)
        self.results_table = ttk.Treeview(self.results_frame.master, columns=self.headers, show='headings')
        self.results_table.grid(row=0, column=0, sticky="nsew")
        
        for record in self.headers:
            self.results_table.column(record, anchor=tk.CENTER, width=100, minwidth=80, stretch=False)
            self.results_table.heading(record, text=record, anchor=tk.CENTER)
        self.results_table.column(self.headers[0], stretch=True)
        
        for record in self.data:
            self.results_table.insert(parent='', index='end', values=record)
            
        self.scrollbar = ttk.Scrollbar(
            self.results_frame.master,
            orient=tk.VERTICAL,
            command=self.results_table.yview,
        )
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.results_table.configure(yscrollcommand=self.scrollbar.set)
        
        self.root.resizable(True, True)
        self.makeResizable()
        self.run()
        
    def update_results(self, _):
        """Updates the results treeview based on the search entry."""
        query = self.query.get()
        matches = search_data(query, self.data)
        self.results_table.delete(*self.results_table.get_children())

        if matches:
            for record in matches:
                self.results_table.insert(parent='', index='end', values=record)
        else:
            if not query:
                for record in self.data:
                    self.results_table.insert(parent='', index='end', values=record)


App()
