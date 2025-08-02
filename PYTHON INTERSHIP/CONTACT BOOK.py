import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
    
    def __hash__(self):
        return hash(self.name.lower())  # Use name as unique identifier
    
    def __eq__(self, other):
        if not isinstance(other, Contact):
            return False
        return self.name.lower() == other.name.lower()
    
    def to_dict(self):
        return {"name": self.name, "phone": self.phone, "email": self.email}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["phone"], data["email"])

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.contacts = set()
        self.file_path = "contacts.json"
        
        # Load contacts from file
        self.load_contacts()
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input fields
        ttk.Label(self.main_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.name_entry = ttk.Entry(self.main_frame, width=30)
        self.name_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(self.main_frame, text="Phone:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.phone_entry = ttk.Entry(self.main_frame, width=30)
        self.phone_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(self.main_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.email_entry = ttk.Entry(self.main_frame, width=30)
        self.email_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # Buttons
        ttk.Button(self.main_frame, text="Add Contact", command=self.add_contact).grid(row=3, column=0, pady=5)
        ttk.Button(self.main_frame, text="Update Contact", command=self.update_contact).grid(row=3, column=1, pady=5)
        ttk.Button(self.main_frame, text="Delete Contact", command=self.delete_contact).grid(row=3, column=2, pady=5)
        
        # Contact list display
        self.tree = ttk.Treeview(self.main_frame, columns=("Name", "Phone", "Email"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        self.tree.column("Name", width=150)
        self.tree.column("Phone", width=100)
        self.tree.column("Email", width=150)
        self.tree.grid(row=4, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=4, column=3, sticky=(tk.N, tk.S))
        
        # Initialize selected contact
        self.selected_contact = None
        
        # Update treeview with loaded contacts
        self.update_treeview()

    def load_contacts(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as file:
                    data = json.load(file)
                    self.contacts = {Contact.from_dict(contact) for contact in data}
            except (json.JSONDecodeError, KeyError):
                messagebox.showwarning("Warning", "Error loading contacts file. Starting with empty contact book.")

    def save_contacts(self):
        try:
            with open(self.file_path, "w") as file:
                json.dump([contact.to_dict() for contact in self.contacts], file, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save contacts: {str(e)}")

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return
        
        new_contact = Contact(name, phone, email)
        if new_contact in self.contacts:
            messagebox.showerror("Error", f"Contact {name} already exists!")
            return
        
        self.contacts.add(new_contact)
        self.update_treeview()
        self.save_contacts()
        self.clear_entries()
        messagebox.showinfo("Success", f"Contact {name} added successfully.")

    def update_contact(self):
        if not self.selected_contact:
            messagebox.showerror("Error", "Please select a contact to update!")
            return
        
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if name and name.lower() != self.selected_contact.name.lower():
            if any(c.name.lower() == name.lower() for c in self.contacts):
                messagebox.showerror("Error", f"Contact {name} already exists!")
                return
        
        self.contacts.remove(self.selected_contact)
        updated_contact = Contact(
            name or self.selected_contact.name,
            phone or self.selected_contact.phone,
            email or self.selected_contact.email
        )
        self.contacts.add(updated_contact)
        self.update_treeview()
        self.save_contacts()
        self.clear_entries()
        self.selected_contact = None
        messagebox.showinfo("Success", "Contact updated successfully.")

    def delete_contact(self):
        if not self.selected_contact:
            messagebox.showerror("Error", "Please select a contact to delete!")
            return
        
        self.contacts.remove(self.selected_contact)
        self.update_treeview()
        self.save_contacts()
        self.clear_entries()
        self.selected_contact = None
        messagebox.showinfo("Success", "Contact deleted successfully.")

    def update_treeview(self):
        # Clear current treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add contacts sorted by name
        for contact in sorted(self.contacts, key=lambda x: x.name):
            self.tree.insert("", tk.END, values=(contact.name, contact.phone, contact.email))

    def on_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            name, phone, email = self.tree.item(item, "values")
            self.selected_contact = self.find_contact(name)
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.name_entry.insert(0, name)
            self.phone_entry.insert(0, phone)
            self.email_entry.insert(0, email)

    def find_contact(self, name):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                return contact
        return None

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()