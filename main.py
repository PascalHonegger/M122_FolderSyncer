#!/usr/bin/python3

# GUI imports
from tkinter import Tk, StringVar, DoubleVar, END, Listbox, NS, EW
from tkinter.ttk import Button, Label, Progressbar, Entry, Scrollbar
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo
# File managements imports
from os import path, walk, makedirs, remove
from filecmp import cmp
from shutil import copy2
# Threading imports
from _thread import start_new_thread

# ---------- Variables ---------- #
window = Tk()
source_path = StringVar()
target_path = StringVar()
progress_value = DoubleVar()
string_added_files = StringVar()
string_changed_files = StringVar()
string_deleted_files = StringVar()
pattern_added_files = "Added {0:d} file(s)"
pattern_changed_files = "Changed {0:d} file(s)"
pattern_deleted_files = "Deleted {0:d} file(s)"

string_added_files.set(pattern_added_files.format(0))
string_changed_files.set(pattern_changed_files.format(0))
string_deleted_files.set(pattern_deleted_files.format(0))


# ------------ Methods ---------- #
def chose_source_folder():
    source_folder = askdirectory(title="Source folder", mustexist=True)
    source_path.set(source_folder)


def chose_target_folder():
    target_folder = askdirectory(title="Target folder", mustexist=True)
    target_path.set(target_folder)


# Calls sync_folders in a new thread
def sync_folders_new_thread():
    start_new_thread(sync_folders, ())


def sync_folders():
    # Validate Source and Target are valid paths
    if not source_path.get():
        showinfo("Source folder required", "Please enter a source folder")
        return

    if not path.isdir(source_path.get()):
        showinfo("Source folder invalid", "Please enter a valid path for the source folder")
        return

    if not target_path.get():
        showinfo("Target folder required", "Please enter a target folder")
        return

    if not path.isdir(target_path.get()):
        showinfo("Target folder invalid", "Please enter a valid path for the target folder")
        return

    # Reset / initialize all arrays
    all_source_files = []
    all_target_files = []
    all_added_files = []
    all_deleted_files = []
    all_changed_files = []
    all_existing_files = []
    progress_value.set(0)

    # Extract relative paths from source and target
    for dirpath, dirnames, filenames in walk(source_path.get()):
        for fileName in filenames:
            full_path = path.join(dirpath, fileName)
            relative_path = path.relpath(full_path, source_path.get())
            all_source_files.append(relative_path)

    for dirpath, dirnames, filenames in walk(target_path.get()):
        for fileName in filenames:
            full_path = path.join(dirpath, fileName)
            relative_path = path.relpath(full_path, target_path.get())
            all_target_files.append(relative_path)

    # Go through relative paths and evaluate, if they were added, changed or removed
    for source_file in all_source_files:
        if source_file in all_target_files:
            all_existing_files.append(source_file)
        else:
            all_added_files.append(source_file)

    for target_file in all_target_files:
        if target_file not in all_source_files:
            all_deleted_files.append(target_file)

    for existing_file in all_existing_files:
        full_source_path = path.join(source_path.get(), existing_file)
        full_target_path = path.join(target_path.get(), existing_file)

        if not cmp(full_source_path, full_target_path):
            all_changed_files.append(existing_file)

    # Write sync status to gui
    string_added_files.set(pattern_added_files.format(len(all_added_files)))
    string_changed_files.set(pattern_changed_files.format(len(all_changed_files)))
    string_deleted_files.set(pattern_deleted_files.format(len(all_deleted_files)))

    # Add changes to history
    if len(all_added_files) > 0:
        file_commit_message = "+ ADDED: "

        for p in all_added_files:
            file_commit_message += p + " "
        listbox.insert(END, file_commit_message)

    if len(all_changed_files) > 0:
        file_commit_message = "~ CHANGED: "

        for p in all_changed_files:
            file_commit_message += p + " "
        listbox.insert(END, file_commit_message)

    if len(all_deleted_files) > 0:
        file_commit_message = "- REMOVED: "

        for p in all_deleted_files:
            file_commit_message += p + " "
        listbox.insert(END, file_commit_message)

    to_be_copied = all_added_files + all_changed_files

    total_changed_items = len(to_be_copied + all_deleted_files)

    if total_changed_items == 0:
        progress_value.set(100)
        return

    step = 100 / total_changed_items

    # Copy and delete files
    for changed_file in to_be_copied:
        full_source_path = path.join(source_path.get(), changed_file)
        full_target_path = path.join(target_path.get(), changed_file)
        if not path.exists(path.dirname(full_target_path)):
            makedirs(path.dirname(full_target_path))
        copy2(full_source_path, full_target_path)
        progress_value.set(progress_value.get() + step)

    for deleted_file in all_deleted_files:
        full_target_path = path.join(target_path.get(), deleted_file)
        remove(full_target_path)
        progress_value.set(progress_value.get() + step)

    progress_value.set(100)


# ------------- GUI ------------- #
# Configure window
window.title("Folder syncer")
window.geometry("560x250")

# Source folder label
Label(window, text="Source folder:").grid(row=0, column=0)

# Source folder entry
Entry(window, textvariable=source_path).grid(row=1, column=0)

# Source folder button
Button(window, command=chose_source_folder, text="Get source folder").grid(row=1, column=1)

# Target folder label
Label(window, text="Target folder:").grid(row=0, column=3)

# Target folder entry
Entry(window, textvariable=target_path).grid(row=1, column=3)

# Target folder button
Button(window, command=chose_target_folder, text="Get target folder").grid(row=1, column=4)

# Sync button
Button(window, command=sync_folders_new_thread, text="<- Sync ->").grid(row=1, column=2)

# Progress bar
Progressbar(window, maximum=100, mode="determinate", length=525, variable=progress_value).grid(row=2, column=0, columnspan=5)

# Sync status added
Label(window, textvariable=string_added_files, foreground="green", justify="left").grid(row=3, column=0)

# Sync status changed
Label(window, textvariable=string_changed_files, foreground="orange", justify="center").grid(row=3, column=2)

# Sync status deleted
Label(window, textvariable=string_deleted_files, foreground="red", justify="right").grid(row=3, column=4)

# Sync history scrollbar
scrollbar = Scrollbar(window)
scrollbar.grid(rowspan=5, column=5, sticky=NS)

# Sync history list
listbox = Listbox(window)
listbox.grid(row=4, columnspan=5, sticky=EW)

# Attach listbox to scrollbar
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Run GUI on main thread
window.mainloop()
