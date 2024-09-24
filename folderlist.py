import os
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser

def get_folder_size(directory):
    """Calculate the total size of the folder by summing the sizes of all its files."""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            for file in filenames:
                file_path = os.path.join(dirpath, file)
                if os.path.exists(file_path):
                    total_size += os.path.getsize(file_path)
    except PermissionError:
        return 0  # If there's a permission error, return 0 for folder size
    return total_size

def format_size(size_in_bytes):
    """Format the size from bytes to a more readable form (KB, MB, GB)."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024

def print_tree(directory, file, prefix=""):
    """Recursively print folder structure to an HTML file with hyperlinks and sizes, handling permission errors."""
    try:
        folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
    except PermissionError:
        file.write(f"{prefix}[Access Denied]<br>\n")
        return

    for i, folder in enumerate(folders):
        folder_path = os.path.join(directory, folder)
        folder_size = get_folder_size(folder_path)
        formatted_size = format_size(folder_size)
        
        # Replace backslashes before formatting the string
        hyperlink_path = folder_path.replace('\\', '/')
        hyperlink = f"file:///{hyperlink_path}"

        if i == len(folders) - 1:
            file.write(f"{prefix}└── <a href=\"{hyperlink}\">{folder}</a> ({formatted_size})<br>\n")
            new_prefix = prefix + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"  # Indent for subfolders
        else:
            file.write(f"{prefix}├── <a href=\"{hyperlink}\">{folder}</a> ({formatted_size})<br>\n")
            new_prefix = prefix + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"  # Indent for subfolders

        print_tree(folder_path, file, new_prefix)



def save_folder_tree_to_html(root_directory, output_file_path):
    """Save the folder structure to an HTML file, skipping directories with permission issues."""
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write("<html><body>\n")
            file.write(f"<h1>Folder structure of: {root_directory}</h1>\n")
            file.write("<pre>\n")  # Preformatted text for tree structure
            print_tree(root_directory, file)
            file.write("</pre>\n")
            file.write("</body></html>")
        messagebox.showinfo("Success", f"Folder structure saved to {output_file_path}")
        webbrowser.open(output_file_path)  # Automatically open the generated HTML file in browser
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def browse_folder():
    """Open a folder dialog to select the root folder."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_selected)

def browse_output_location():
    """Open a dialog to select the output folder location."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_location_entry.delete(0, tk.END)
        output_location_entry.insert(0, folder_selected)

def generate_tree():
    """Generate the folder tree based on user input."""
    root_directory = folder_entry.get()
    output_location = output_location_entry.get()
    output_file_name = file_name_entry.get()

    if not root_directory or not output_location or not output_file_name:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    # Ensure the output file has an .html extension
    if not output_file_name.endswith(".html"):
        output_file_name += ".html"

    output_file_path = os.path.join(output_location, output_file_name)
    
    save_folder_tree_to_html(root_directory, output_file_path)

# Create the main application window
root = tk.Tk()
root.title("Folder Tree Generator with Sizes and Hyperlinks")

# Input fields and labels
tk.Label(root, text="Select Folder/Drive:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
folder_entry = tk.Entry(root, width=50)
folder_entry.grid(row=0, column=1, padx=10, pady=10)
browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Output Location:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
output_location_entry = tk.Entry(root, width=50)
output_location_entry.grid(row=1, column=1, padx=10, pady=10)
output_browse_button = tk.Button(root, text="Browse", command=browse_output_location)
output_browse_button.grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="Output File Name:").grid(row=2, column=0, padx=10, pady=10, sticky='w')
file_name_entry = tk.Entry(root, width=50)
file_name_entry.grid(row=2, column=1, padx=10, pady=10)

# Generate button
generate_button = tk.Button(root, text="Generate Folder Tree", command=generate_tree)
generate_button.grid(row=3, column=0, columnspan=3, pady=20)

# Start the application
root.mainloop()
