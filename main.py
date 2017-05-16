#!/usr/bin/python3

from tkinter import Tk, Text, DISABLED, END
from tkinter.ttk import Button, Label, Progressbar
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo

window = Tk()


window.title("Dummy")
window.geometry("400x200")

label = Label(window, text="Dummy text!")
label.pack()

progress = Progressbar(window, maximum=100, mode="determinate", length=500)
progress.pack()


def button_click():
    window.title("HAHA")
    progress.start(100)


button = Button(window, command=button_click, text="Set title!")
button.pack()

source_text = Text(window, state=DISABLED, height=1, width=50)
source_text.pack()


def chose_source_folder():
    source_folder = askdirectory(title="Source folder", mustexist=True)
    source_text.delete("1.0", END)
    source_text.insert("1.0", source_folder)
    showinfo("Selected folder", source_folder)


button = Button(window, command=chose_source_folder, text="Get folder!")
button.pack()

window.mainloop()
