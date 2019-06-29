from tkinter import *
from tkinter.scrolledtext import *
from tkinter.filedialog import *
from gds import *

root = Tk(className=" GDS Editor")
textPad = ScrolledText(root, width=300, height=80)

lastFile = 0

def filemenu_new():
    global lastFile
    lastFile = 0
    textPad.insert('1.0', "")

def filemenu_open():
    global lastFile
    filename = askopenfilename(title="Open GDS file", filetypes=(("GDS Script", "*.gds"), ("All Files", "*.*")))
    if not filename:
        return
    lastFile = filename
    root.title(filename)
    with open(filename, 'rb') as file:
        textPad.insert('1.0', convert_to_simplified(extract_from_gds(file.read())))

def filemenu_save():
    global lastFile
    filename = lastFile
    if not filename:
        filemenu_saveas()
        return
    with open(filename, 'wb+') as file:
        file.write(convert_to_gds(extract_from_simplified(textPad.get('1.0', END))))

def filemenu_saveas():
    global lastFile
    filename = asksaveasfilename(title="Save GDS file", filetypes=(("GDS Script", "*.gds"), ("All Files", "*.*")))
    lastFile = filename
    root.title(filename)
    if not filename:
        return
    with open(filename, 'wb+') as file:
        file.write(convert_to_gds(extract_from_simplified(textPad.get('1.0', END))))



def dummy():
    return

textPad.pack()
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=dummy)
filemenu.add_command(label="Open...", command=filemenu_open)
filemenu.add_command(label="Save", command=filemenu_save)
filemenu.add_command(label="Save As", command=filemenu_saveas)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=dummy)
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=dummy)
root.geometry("800x600")
root.mainloop()