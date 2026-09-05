import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


# File categories and their extensions
FILE_CATEGORIES = {
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp",
        ".webp", ".svg", ".tiff", ".ico"
    ],

    "Documents": [
        ".pdf", ".doc", ".docx", ".txt", ".rtf",
        ".odt"
    ],

    "Spreadsheets": [
        ".xls", ".xlsx", ".csv", ".ods"
    ],

    "Presentations": [
        ".ppt", ".pptx", ".odp"
    ],

    "Videos": [
        ".mp4", ".mkv", ".avi", ".mov",
        ".wmv", ".flv", ".webm"
    ],

    "Audio": [
        ".mp3", ".wav", ".aac", ".flac",
        ".ogg", ".m4a"
    ],

    "Archives": [
        ".zip", ".rar", ".7z", ".tar",
        ".gz", ".bz2"
    ],

    "Programs": [
        ".exe", ".msi", ".apk", ".bat",
        ".sh", ".py", ".java", ".cpp",
        ".c", ".js"
    ]
}


def get_category(extension):
    """
    Returns the category of a file based on its extension.
    """

    extension = extension.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


def get_unique_filename(destination_folder, filename):
    """
    Prevents overwriting files with the same name.
    """

    name, extension = os.path.splitext(filename)

    new_filename = filename
    counter = 1

    while os.path.exists(os.path.join(destination_folder, new_filename)):
        new_filename = f"{name}_{counter}{extension}"
        counter += 1

    return new_filename


def organize_files(folder_path):
    """
    Scans the selected folder and moves files
    into category folders.
    """

    if not folder_path:
        return

    if not os.path.isdir(folder_path):
        messagebox.showerror(
            "Error",
            "The selected folder does not exist."
        )
        return

    log_box.delete("1.0", tk.END)

    moved_count = 0

    try:
        # Get files from selected directory
        files = os.listdir(folder_path)

        for filename in files:

            source_path = os.path.join(folder_path, filename)

            # Ignore directories
            if os.path.isdir(source_path):
                continue

            # Get file extension
            extension = os.path.splitext(filename)[1]

            # Determine category
            category = get_category(extension)

            # Create category folder
            destination_folder = os.path.join(
                folder_path,
                category
            )

            os.makedirs(
                destination_folder,
                exist_ok=True
            )

            # Generate unique filename
            new_filename = get_unique_filename(
                destination_folder,
                filename
            )

            destination_path = os.path.join(
                destination_folder,
                new_filename
            )

            # Move file
            shutil.move(
                source_path,
                destination_path
            )

            log_box.insert(
                tk.END,
                f"✓ {filename} → {category}/{new_filename}\n"
            )

            moved_count += 1

        log_box.insert(
            tk.END,
            "\n--------------------------------\n"
        )

        log_box.insert(
            tk.END,
            f"Successfully organized {moved_count} file(s).\n"
        )

        messagebox.showinfo(
            "Completed",
            f"Successfully organized {moved_count} file(s)!"
        )

    except PermissionError:
        messagebox.showerror(
            "Permission Error",
            "You don't have permission to modify this folder."
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"Something went wrong:\n{error}"
        )


def select_folder():
    """
    Opens folder selection dialog.
    """

    folder = filedialog.askdirectory(
        title="Select Folder to Organize"
    )

    if folder:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)


def start_organizing():
    """
    Starts the file organization process.
    """

    folder = folder_entry.get().strip()

    if not folder:
        messagebox.showwarning(
            "Warning",
            "Please select a folder first."
        )
        return

    organize_files(folder)


# -----------------------------
# GUI
# -----------------------------

root = tk.Tk()

root.title("File Organizer")
root.geometry("750x550")
root.resizable(False, False)


# Title
title_label = tk.Label(
    root,
    text="📁 File Organizer",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=20)


# Description
description_label = tk.Label(
    root,
    text="Select a folder and automatically organize your files.",
    font=("Arial", 11)
)

description_label.pack(pady=5)


# Folder frame
folder_frame = tk.Frame(root)

folder_frame.pack(pady=20)


folder_entry = tk.Entry(
    folder_frame,
    width=55,
    font=("Arial", 11)
)

folder_entry.grid(
    row=0,
    column=0,
    padx=5
)


browse_button = tk.Button(
    folder_frame,
    text="Browse",
    command=select_folder,
    width=12
)

browse_button.grid(
    row=0,
    column=1,
    padx=5
)


# Organize button
organize_button = tk.Button(
    root,
    text="🚀 Organize Files",
    command=start_organizing,
    font=("Arial", 13, "bold"),
    width=20,
    height=2
)

organize_button.pack(pady=10)


# Log label
log_label = tk.Label(
    root,
    text="Organization Log",
    font=("Arial", 13, "bold")
)

log_label.pack(pady=10)


# Log box
log_box = scrolledtext.ScrolledText(
    root,
    width=85,
    height=18,
    font=("Consolas", 10)
)

log_box.pack(
    padx=20,
    pady=5
)


# Footer
footer = tk.Label(
    root,
    text="File Organizer • Python Project",
    font=("Arial", 9)
)

footer.pack(
    side=tk.BOTTOM,
    pady=10
)


# Start application
root.mainloop()