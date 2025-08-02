import tkinter as tk
from tkinter import messagebox
import random
import string

# Function to generate password
def generate_password():
    length = int(length_entry.get())

    characters = ""
    if var_letters.get():
        characters += string.ascii_letters
    if var_digits.get():
        characters += string.digits
    if var_symbols.get():
        characters += string.punctuation

    if characters == "":
        messagebox.showwarning("Warning", "Select at least one character type!")
        return

    password = ''.join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# Function to copy password to clipboard
def copy_to_clipboard():
    password = password_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

# Create GUI window
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x300")
root.resizable(False, False)

# Title
title = tk.Label(root, text="Secure Password Generator", font=("Arial", 16, "bold"))
title.pack(pady=10)

# Length selection
frame = tk.Frame(root)
frame.pack(pady=5)
tk.Label(frame, text="Password Length: ", font=("Arial", 12)).pack(side=tk.LEFT)
length_entry = tk.Entry(frame, width=5, font=("Arial", 12))
length_entry.insert(0, "12")
length_entry.pack(side=tk.LEFT)

# Checkboxes for options
var_letters = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Letters", variable=var_letters, font=("Arial", 11)).pack()
tk.Checkbutton(root, text="Include Numbers", variable=var_digits, font=("Arial", 11)).pack()
tk.Checkbutton(root, text="Include Symbols", variable=var_symbols, font=("Arial", 11)).pack()

# Entry to show password
password_entry = tk.Entry(root, font=("Arial", 14), justify="center", width=30)
password_entry.pack(pady=10)

# Buttons
tk.Button(root, text="Generate Password", command=generate_password, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=5)
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, font=("Arial", 12), bg="#2196F3", fg="white").pack(pady=5)

# Start GUI loop
root.mainloop()
