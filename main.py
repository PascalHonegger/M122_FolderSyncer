#!/usr/bin/python3

from tkinter import Tk, Text, DISABLED, END
from tkinter.ttk import Button, Label, Progressbar
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo

window = Tk()

window.title("Folder syncer")
window.geometry("400x200")

source_label = Label(window, text="Source folder:")
source_label.grid(row=0, column=0, columnspan=2)

source_text = Text(window, height=1, width=50)
source_text.grid(row=1, column=0)


def chose_source_folder():
    source_folder = askdirectory(title="Source folder", mustexist=True)
    source_text.delete("1.0", END)
    source_text.insert("1.0", source_folder)


chose_source_button = Button(window, command=chose_source_folder, text="Get source folder")
chose_source_button.grid(row=1, column=1)

target_label = Label(window, text="Target folder:")
target_label.grid(row=0, column=3)

target_text = Text(window, height=1, width=50)
target_text.grid(row=1, column=3)


def chose_target_folder():
    source_folder = askdirectory(title="Target folder", mustexist=False)
    target_text.delete("1.0", END)
    target_text.insert("1.0", source_folder)


chose_target_button = Button(window, command=chose_target_folder, text="Get target folder")
chose_target_button.grid(row=1, column=4)

sync_button = Button(window, command=chose_target_folder, text="<- Sync ->")
sync_button.grid(row=1, column=2)

progress = Progressbar(window, maximum=100, mode="determinate", length=500)
progress.grid(row=2, column=0, columnspan=5)

window.mainloop()
