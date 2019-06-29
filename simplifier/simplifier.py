import gds
import sys
import tkinter.filedialog

root = tkinter.Tk()
root.withdraw()

input_filename = tkinter.filedialog.askopenfilename(filetypes=(("Text File", "*.gds"), ("All Files", "*.*")),
                                                title="Open")
if len(input_filename) < 1:
    sys.exit()

with open(input_filename, "rb") as file:
    data = file.read()

ext = gds.extract_from_gds(data)

output_filename = tkinter.filedialog.asksaveasfilename(filetypes=(("Text File", "*.txt"), ("All Files", "*.*")),
                                                title="Open")
if len(output_filename) < 1:
    sys.exit()

if not "." in output_filename:
    output_filename += ".txt"

with open(output_filename, "w+") as file:
    file.write(gds.convert_to_simplified(ext))
