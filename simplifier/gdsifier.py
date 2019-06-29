import gds
import sys
import tkinter.filedialog

root = tkinter.Tk()
root.withdraw()

input_filename = tkinter.filedialog.askopenfilename(filetypes=(("Text File", "*.txt"), ("All Files", "*.*")),
                                                title="Open")
if len(input_filename) < 1:
    sys.exit()

with open(input_filename, "r") as file:
    data = file.read()

ext = gds.extract_from_simplified(data)

output_filename = tkinter.filedialog.asksaveasfilename(filetypes=(("Text File", "*.gds"), ("All Files", "*.*")),
                                                title="Open")
if len(output_filename) < 1:
    sys.exit()

if not "." in output_filename:
    output_filename += ".gds"

print(ext)

with open(output_filename, "wb+") as file:
    file.write(gds.convert_to_gds(ext))