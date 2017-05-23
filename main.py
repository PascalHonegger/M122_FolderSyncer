#!/usr/bin/python3
import os
from tkinter import Tk, StringVar
from tkinter.ttk import Button, Label, Progressbar, Entry
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo
from filecmp import cmp
from shutil import copy2

window = Tk()

window.title("Folder syncer")
window.geometry("525x75")

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

    for dirpath, dirnames, filenames in os.walk(source_path.get()):
        for fileName in filenames:
            full_path = os.path.join(dirpath, fileName)
            relative_path = os.path.relpath(full_path, source_path.get())
            all_source_files.append(relative_path)

    all_target_files = []

    for dirpath, dirnames, filenames in os.walk(target_path.get()):
        for fileName in filenames:
            full_path = os.path.join(dirpath, fileName)
            relative_path = os.path.relpath(full_path, target_path.get())
            all_target_files.append(relative_path)

    all_added_files = []
    all_deleted_files = []
    all_changed_files = []

    all_existing_files = []

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

    #TODO compare content
    print(all_added_files)
    print(all_existing_files)
    print(all_changed_files)
    print(all_deleted_files)

    to_be_copied = all_added_files + all_changed_files

    # TODO check folder structure

    step = 100 / len(to_be_copied + all_deleted_files)

    for changed_file in to_be_copied:
        full_source_path = os.path.join(source_path.get(), changed_file)
        full_target_path = os.path.join(target_path.get(), changed_file)
        if not os.path.exists(os.path.dirname(full_target_path)):
            os.makedirs(os.path.dirname(full_target_path))
        copy2(full_source_path, full_target_path)
        progress.step(step)
        progress.update()

    for deleted_file in all_deleted_files:
        full_target_path = os.path.join(target_path.get(), deleted_file)
        os.remove(full_target_path)
        progress.step(step)
        progress.update()


sync_button = Button(window, command=sync_folders, text="<- Sync ->")
sync_button.grid(row=1, column=2)

progress = Progressbar(window, maximum=100, mode="determinate", length=525)
progress.grid(row=2, column=0, columnspan=5)

window.mainloop()
