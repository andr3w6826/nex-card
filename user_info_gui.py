import tkinter as tk
from tkinter import messagebox
import json
import os
import sys
import platform
import subprocess

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "users.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    else:
        with open(DATA_FILE, "w") as file:
            json.dump({}, file)
            return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def load_prompt_user():
    name = entry_name.get().strip()
    if not name:
        messagebox.showwarning("Missing name", "Please enter your name.")
        return

    data = load_data()
    if name in data:
        entry_expend.delete(0, tk.END)
        entry_food_expend.delete(0, tk.END)
        entry_travel_expend.delete(0, tk.END)
        entry_expend.insert(0, data[name]["expenditure"])
        entry_food_expend.insert(0, data[name]["food_expend"])
        entry_travel_expend.insert(0, data[name]["travel_expend"])
        messagebox.showinfo("Welcome back!", f"Loaded existing data for {name}.")
    else:
        messagebox.showinfo("New user", f"No existing data for {name}. You can create a new profile.")

def save_user():
    name = entry_name.get().strip()
    expend = entry_expend.get().strip()
    food_expend = entry_food_expend.get().strip()
    travel_expend = entry_travel_expend.get().strip()

    if not name or not expend or not food_expend or not travel_expend:
        messagebox.showwarning("Missing info", "Please fill in all fields.")
        return

    data = load_data()
    data[name] = {"expenditure": expend, "food_expend": food_expend, "travel_expend": travel_expend}
    save_data(data)
    messagebox.showinfo("Success", f"Data for {name} saved successfully!")

def open_data_folder():
    folder = os.path.dirname(DATA_FILE)
    if platform.system() == "Windows":
        os.startfile(folder)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", folder])
    else:  # Linux
        subprocess.run(["xdg-open", folder])

root = tk.Tk()
root.title("User Data Collection")
root.geometry("400x300")
root.resizable(False, False)

# Labels
tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
tk.Label(root, text="Monthly Expenditure:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
tk.Label(root, text="Monthly Food Expense:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
tk.Label(root, text="Monthly Travel Expense:").grid(row=3, column=0, padx=10, pady=10, sticky="e")

# Entries
entry_name = tk.Entry(root, width=25)
entry_expend = tk.Entry(root, width=25)
entry_food_expend = tk.Entry(root, width=25)
entry_travel_expend = tk.Entry(root, width=25)
entry_name.grid(row=0, column=1)
entry_expend.grid(row=1, column=1)
entry_food_expend.grid(row=2, column=1)
entry_travel_expend.grid(row=3, column=1)

# Buttons
tk.Button(root, text="Load User", command=load_prompt_user).grid(row=4, column=0, pady=20)
tk.Button(root, text="Save User", command=save_user).grid(row=4, column=1, pady=20)
tk.Button(root, text="Open Data Folder", command=open_data_folder).grid(row=5, column=0, pady=20)
root.mainloop()
