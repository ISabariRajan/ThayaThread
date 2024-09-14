import tkinter as tk
from tkinter import messagebox, filedialog
from guifunctions import GUIFunctions

guifunctions = GUIFunctions()


root = tk.Tk()
root.title("Thaya thread GUI App")
root.geometry("1000x1000")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

heading = tk.Label(root, text="Image Modifier", font=("Helvetica", 24))
heading.grid(row=0, column=0, padx=50, pady=50)

image_canvas_1 = tk.Canvas(root, width=300, height=300)
image_canvas_1.grid(row=1, column=0, padx=30, pady=30)
image_canvas_2 = tk.Canvas(root, width=300, height=300)
image_canvas_2.grid(row=1, column=1, padx=30, pady=30)

select_folder_button = tk.Button(root, text="Select Folder", command=lambda: guifunctions.file_dialog())
select_folder_button.grid(row=2, column=0, padx=50, pady=30)

update_button = tk.Button(root, text="Download", command=lambda: guifunctions.download())
update_button.grid(row=2, column=1, padx=50, pady=30)

exit_button = tk.Button(root, text="Exit", command=lambda: guifunctions.download())
exit_button.grid(row=2, column=2, padx=50, pady=30)

root.mainloop()