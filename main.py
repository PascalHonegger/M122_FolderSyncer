#!/usr/bin/python3
import os
from tkinter import Tk, StringVar, DoubleVar, END, Listbox, NS, EW
from tkinter.ttk import Button, Label, Progressbar, Entry, Scrollbar
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo
from filecmp import cmp
from shutil import copy2

from _thread import start_new_thread

window = Tk()

window.title("Folder syncer")
window.geometry("550x250")

source_label = Label(window, text="Source folder:")
source_label.grid(row=0, column=0, columnspan=2)

source_path = StringVar()
source_text = Entry(window, textvariable=source_path)
source_text.grid(row=1, column=0)


def chose_source_folder():
    source_folder = askdirectory(title="Source folder", mustexist=True)
    source_path.set(source_folder)

chose_source_button = Button(window, command=chose_source_folder, text="Get source folder")
chose_source_button.grid(row=1, column=1)

target_label = Label(window, text="Target folder:")
target_label.grid(row=0, column=3)

target_path = StringVar()
target_text = Entry(window, textvariable=target_path)
target_text.grid(row=1, column=3)


def chose_target_folder():
    target_folder = askdirectory(title="Target folder", mustexist=True)
    target_path.set(target_folder)


chose_target_button = Button(window, command=chose_target_folder, text="Get target folder")
chose_target_button.grid(row=1, column=4)


def sync_folders_new_thread():
    start_new_thread(sync_folders, ())


def sync_folders():
    if not source_path.get():
        showinfo("Source folder required", "Please enter a source folder")
        return

    if not os.path.isdir(source_path.get()):
        showinfo("Source folder invalid", "Please enter a valid path for the source folder")
        return

    if not target_path.get():
        showinfo("Target folder required", "Please enter a target folder")
        return

    if not os.path.isdir(target_path.get()):
        showinfo("Target folder invalid", "Please enter a valid path for the target folder")
        return

    all_source_files = []
    all_target_files = []
    all_added_files = []
    all_deleted_files = []
    all_changed_files = []
    all_existing_files = []
    progress_value.set(0)

    for dirpath, dirnames, filenames in os.walk(source_path.get()):
        for fileName in filenames:
            full_path = os.path.join(dirpath, fileName)
            relative_path = os.path.relpath(full_path, source_path.get())
            all_source_files.append(relative_path)

    for dirpath, dirnames, filenames in os.walk(target_path.get()):
        for fileName in filenames:
            full_path = os.path.join(dirpath, fileName)
            relative_path = os.path.relpath(full_path, target_path.get())
            all_target_files.append(relative_path)

    for source_file in all_source_files:
        if source_file in all_target_files:
            all_existing_files.append(source_file)
        else:
            all_added_files.append(source_file)

    for target_file in all_target_files:
        if target_file not in all_source_files:
            all_deleted_files.append(target_file)

    for existing_file in all_existing_files:
        full_source_path = os.path.join(source_path.get(), existing_file)
        full_target_path = os.path.join(target_path.get(), existing_file)

        if not cmp(full_source_path, full_target_path):
            all_changed_files.append(existing_file)

    added_label.config(text="Added " + str(len(all_added_files)) + " files")
    changed_label.config(text="Changed " + str(len(all_changed_files)) + " files")
    deleted_label.config(text="Removed " + str(len(all_deleted_files)) + " files")

    if len(all_added_files) > 0:
        file_commit_message = "ADDED: "

        for p in all_added_files:
            file_commit_message += p + " "
        listbox.insert(END, file_commit_message)

    if len(all_changed_files) > 0:
        file_commit_message = "CHANGED: "

        for p in all_changed_files:
            file_commit_message += p + " "
        listbox.insert(END, file_commit_message)

    if len(all_deleted_files) > 0:
        file_commit_message = "REMOVED: "

        for p in all_deleted_files:
            file_commit_message += p + " "
        listbox.insert(END, file_commit_message)


    to_be_copied = all_added_files + all_changed_files

    total_changed_items = len(to_be_copied + all_deleted_files);

    if total_changed_items == 0:
        progress_value.set(100)
        return

    step = 100 / total_changed_items

    for changed_file in to_be_copied:
        full_source_path = os.path.join(source_path.get(), changed_file)
        full_target_path = os.path.join(target_path.get(), changed_file)
        if not os.path.exists(os.path.dirname(full_target_path)):
            os.makedirs(os.path.dirname(full_target_path))
        copy2(full_source_path, full_target_path)
        progress_value.set(progress_value.get() + step)

    for deleted_file in all_deleted_files:
        full_target_path = os.path.join(target_path.get(), deleted_file)
        os.remove(full_target_path)
        progress_value.set(progress_value.get() + step)

    progress_value.set(100)

sync_button = Button(window, command=sync_folders_new_thread, text="<- Sync ->")
sync_button.grid(row=1, column=2)

progress_value = DoubleVar()
progress = Progressbar(window, maximum=100, mode="determinate", length=525, variable=progress_value)
progress.grid(row=2, column=0, columnspan=5)

added_label = Label(window, text="Added 0 files", foreground="green", justify="left")
added_label.grid(row=3, column=0)

changed_label = Label(window, text="Changed 0 files", foreground="orange", justify="center")
changed_label.grid(row=3, column=2)

deleted_label = Label(window, text="Deleted 0 files", foreground="red", justify="right")
deleted_label.grid(row=3, column=4)


scrollbar = Scrollbar(window)
scrollbar.grid(rowspan=5, column=5, sticky=NS)

listbox = Listbox(window)
listbox.grid(row=4, columnspan=5, sticky=EW)

# attach listbox to scrollbar
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)


window.mainloop()
