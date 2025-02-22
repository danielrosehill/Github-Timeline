import tkinter as tk
from tkinter import ttk, messagebox
import os
import re
from pathlib import Path

class CategoryManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Repository Category Manager")
        
        # Set window size and make it resizable
        self.root.geometry("1400x700")  # Increased width
        self.root.minsize(1200, 600)    # Increased min width
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use clam theme for better looking widgets
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
        self.style.configure('TButton', padding=8, font=('Helvetica', 10, 'bold'))
        self.style.configure('Save.TButton', background='#4CAF50', foreground='white')
        self.style.configure('New.TButton', background='#2196F3', foreground='white')
        self.style.configure('TLabelframe', background='#f0f0f0', font=('Helvetica', 10, 'bold'))
        self.style.configure('TLabelframe.Label', font=('Helvetica', 11, 'bold'))
        
        # Get base path
        self.base_path = Path(__file__).parent.parent
        
        # Load data
        self.repos = self.load_repos()
        self.categories = self.load_categories()
        self.category_assignments = self.load_current_assignments()
        
        # Create main layout
        self.create_gui()
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-s>', lambda e: self.save_changes())
        self.root.bind('<Control-f>', lambda e: self.search_entry.focus())
        self.root.bind('<Control-n>', lambda e: self.show_new_category_dialog())
        
        # Populate repos
        self.populate_repos()
        
    def load_repos(self):
        """Load repositories from data/repos.txt"""
        repos = []
        print(f"Loading repos from: {self.base_path / 'data' / 'repos.txt'}")  # Debug print
        try:
            with open(self.base_path / "data" / "repos.txt", "r") as f:
                print("File opened successfully")  # Debug print
                for line in f:
                    # Handle "line_number | repo_name" format
                    repo = line.split('|')[1].strip() if '|' in line else line.strip()
                    print(f"Processing line: '{line.strip()}' -> '{repo}'")  # Debug print
                    if repo:
                        repos.append(repo)
        except Exception as e:
            print(f"Error loading repos from {self.base_path / 'data' / 'repos.txt'}: {e}")
        return repos
    
    def load_categories(self):
        print("Loading categories...")  # Debug print
        """Load available categories from lists/categories directory"""
        categories = []
        try:
            category_dir = self.base_path / "lists" / "categories"
            for file in os.listdir(category_dir):
                if file.endswith('.txt'):
                    categories.append(file[:-4])  # Remove .txt extension
        except Exception as e:
            print(f"Error loading categories: {e}")
        return sorted(categories)  # Sort categories alphabetically
    
    def load_current_assignments(self):
        """Load current category assignments"""
        assignments = {repo: [] for repo in self.repos}
        
        for category in self.categories:
            try:
                with open(self.base_path / "lists" / "categories" / f"{category}.txt", "r") as f:
                    print(f"Loading category: {category}")  # Debug print
                    repos = [line.split('|')[1].strip() if '|' in line else line.strip() for line in f if line.strip()]
                    for repo in repos:
                        if repo in assignments:
                            assignments[repo].append(category)
            except Exception as e:
                print(f"Error loading assignments for {category}: {e}")
        return assignments
    
    def create_gui(self):
        # Create main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Create search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Search:", font=('Helvetica', 10, 'bold')).grid(row=0, column=0, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_repos)
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=('Helvetica', 10))
        self.search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Create repository frame
        repo_frame = ttk.LabelFrame(main_frame, text="Repositories", padding="8")
        repo_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        repo_frame.columnconfigure(0, weight=1)
        repo_frame.rowconfigure(0, weight=1)
        
        # Create repository listbox with scrollbar
        self.repo_listbox = tk.Listbox(repo_frame, selectmode=tk.SINGLE, 
                                     font=('Helvetica', 10),
                                     activestyle='none',  # Remove underline from selected item
                                     width=60,  # Increased width
                                     background='white',
                                     selectbackground='#0078D7',
                                     selectforeground='white')
        self.repo_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        repo_scrollbar = ttk.Scrollbar(repo_frame, orient=tk.VERTICAL, 
                                     command=self.repo_listbox.yview)
        repo_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.repo_listbox.configure(yscrollcommand=repo_scrollbar.set)
        self.repo_listbox.bind('<<ListboxSelect>>', self.on_repo_select)
        
        # Create categories frame
        cat_container = ttk.Frame(main_frame)
        cat_container.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        cat_container.columnconfigure(0, weight=1)
        cat_container.rowconfigure(1, weight=1)
        
        # Categories header with New Category button
        cat_header = ttk.Frame(cat_container)
        cat_header.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        ttk.Label(cat_header, text="Categories", font=('Helvetica', 11, 'bold')).pack(side=tk.LEFT)
        new_cat_btn = ttk.Button(cat_header, text="New Category (Ctrl+N)", 
                               command=self.show_new_category_dialog,
                               style='New.TButton')
        new_cat_btn.pack(side=tk.RIGHT)
        
        # Categories content
        cat_frame = ttk.Frame(cat_container)
        cat_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        cat_frame.columnconfigure(0, weight=1)
        
        # Create canvas and scrollbar for categories
        cat_canvas = tk.Canvas(cat_frame, background='#f0f0f0', highlightthickness=0)
        cat_scrollbar = ttk.Scrollbar(cat_frame, orient=tk.VERTICAL, 
                                    command=cat_canvas.yview)
        self.cat_scrollable_frame = ttk.Frame(cat_canvas)  # Make it instance variable
        
        self.cat_scrollable_frame.bind(
            "<Configure>",
            lambda e: cat_canvas.configure(scrollregion=cat_canvas.bbox("all"))
        )
        
        cat_canvas.create_window((0, 0), window=self.cat_scrollable_frame, anchor=tk.NW)
        cat_canvas.configure(yscrollcommand=cat_scrollbar.set)
        
        # Create checkbuttons for categories
        self.category_vars = {}
        for i, category in enumerate(self.categories):
            var = tk.BooleanVar()
            self.category_vars[category] = var
            frame = ttk.Frame(self.cat_scrollable_frame)
            frame.pack(fill=tk.X, pady=1)
            if i % 2 == 0:
                frame.configure(style='Even.TFrame')
            
            cb = ttk.Checkbutton(frame, text=category, variable=var)
            cb.pack(anchor=tk.W, pady=2, padx=5)
        
        cat_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        cat_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Create status label
        self.status_label = ttk.Label(main_frame, text="", font=('Helvetica', 10))
        self.status_label.grid(row=2, column=0, columnspan=2, pady=(10, 5))
        
        # Create save button
        save_button = ttk.Button(main_frame, text="Save Changes (Ctrl+S)", 
                               command=self.save_changes, style='Save.TButton')
        save_button.grid(row=3, column=0, columnspan=2, pady=(5, 0))
        
        # Add keyboard shortcut hints
        shortcuts_text = "Shortcuts: Ctrl+S (Save), Ctrl+F (Search), Ctrl+N (New Category)"
        shortcuts_label = ttk.Label(main_frame, text=shortcuts_text, 
                                  font=('Helvetica', 9), foreground='#666')
        shortcuts_label.grid(row=4, column=0, columnspan=2, pady=(5, 0))
        
    def show_new_category_dialog(self):
        """Show dialog to create a new category"""
        dialog = tk.Toplevel(self.root)
        dialog.title("New Category")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Create and pack widgets
        ttk.Label(dialog, text="Enter new category name:", 
                 font=('Helvetica', 10, 'bold')).pack(pady=(20, 5))
        
        name_var = tk.StringVar()
        name_entry = ttk.Entry(dialog, textvariable=name_var, width=40)
        name_entry.pack(pady=5, padx=20)
        
        def validate_and_create():
            name = name_var.get().strip().lower()
            if not name:
                messagebox.showwarning("Invalid Name", "Category name cannot be empty.")
                return
            
            if not re.match(r'^[a-z0-9-]+$', name):
                messagebox.showwarning(
                    "Invalid Name",
                    "Category name can only contain lowercase letters, numbers, and hyphens."
                )
                return
            
            if name in self.categories:
                messagebox.showwarning("Duplicate", f"Category '{name}' already exists.")
                return
            
            try:
                # Create new category file
                with open(self.base_path / "lists" / "categories" / f"{name}.txt", "w") as f:
                    pass
                
                # Update GUI
                self.categories = self.load_categories()
                var = tk.BooleanVar()
                self.category_vars[name] = var
                
                frame = ttk.Frame(cat_scrollable_frame)
                frame.pack(fill=tk.X, pady=1)
                cb = ttk.Checkbutton(frame, text=name, variable=var)
                cb.pack(anchor=tk.W, pady=2, padx=5)
                
                # Show success message
                self.status_label.configure(
                    text=f"✓ New category '{name}' created successfully",
                    foreground='#2E7D32'
                )
                
                dialog.destroy()
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create category: {str(e)}")
        
        ttk.Button(dialog, text="Create", command=validate_and_create).pack(pady=20)
        
        # Focus the entry and bind Enter key
        name_entry.focus_set()
        dialog.bind('<Return>', lambda e: validate_and_create())

    def filter_repos(self, *args):
        """Filter repositories based on search text"""
        search_text = self.search_var.get().lower()
        self.repo_listbox.delete(0, tk.END)
        for repo in self.repos:
            if search_text in repo.lower():
                self.repo_listbox.insert(tk.END, repo)
    
    def populate_repos(self):
        """Populate the repository listbox"""
        for repo in self.repos:
            print(f"Adding to listbox: {repo}")  # Debug print
            self.repo_listbox.insert(tk.END, repo)
        self.repo_listbox.update()  # Force update
        print(f"Total repos added: {self.repo_listbox.size()}")  # Debug print
    
    def on_repo_select(self, event):
        """Handle repository selection"""
        selection = self.repo_listbox.curselection()
        if not selection:
            return
        
        repo = self.repo_listbox.get(selection[0])
        # Update checkboxes based on current assignments
        for category, var in self.category_vars.items():
            var.set(category in self.category_assignments.get(repo, []))
        
        # Clear status message when selecting new repo
        self.status_label.configure(text="")
    
    def save_changes(self):
        """Save category assignments back to files"""
        # Get current repo selection
        selection = self.repo_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a repository first.")
            return
            
        repo = self.repo_listbox.get(selection[0])
        
        # Update assignments for the current repo
        self.category_assignments[repo] = [
            category for category, var in self.category_vars.items()
            if var.get()
        ]
        
        # Save to files
        try:
            for category in self.categories:
                repos_in_category = [
                    repo for repo, categories in self.category_assignments.items()
                    if category in categories
                ]
                
                with open(self.base_path / "lists" / "categories" / f"{category}.txt", "w") as f:
                    for repo in sorted(repos_in_category):  # Sort repos alphabetically
                        f.write(f"{repo}\n")
            
            # Show success message
            self.status_label.configure(
                text=f"✓ Categories saved successfully for '{repo}'",
                foreground='#2E7D32'
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {str(e)}")

def main():
    root = tk.Tk()
    app = CategoryManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()