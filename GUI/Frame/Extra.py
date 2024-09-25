import tkinter as tk
from tkinter import Tk, Frame, StringVar, Label, OptionMenu, LabelFrame, Entry, Scrollbar, Canvas
from tkinter import messagebox, filedialog
from tkinter.font import families
from pathlib import Path
from os import listdir
from os.path import join as joinpath, dirname
from tkinter import filedialog
from VideoGenerator.guioperations import GUIOperations
from VideoGenerator.videogenerator import VideoGenerator
# from guifunctions import GUIFunctions
from VideoGenerator.image_operations import list_images_in_folder, resize_image_by_width, \
  draw_overlay, open_rgba_image, new_layer, create_text_image, add_fill_background
from PIL import ImageTk

from json import loads, dumps
from types import SimpleNamespace
from GUI.globals import shared_object, create_heading_label, label_font


class ExtraFrame:
  obj = shared_object

  def generate_frame(self, root):
    frame = Frame(root)
    frame.grid(row=0, column=0, sticky="nw", columnspan=5)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    # Set grid_propagate to False to allow 5-by-5 buttons resizing later
    frame.grid_propagate(False)
    create_heading_label(frame, "Fonts")

    canvas = Canvas(frame, highlightbackground="green", highlightthickness=2)
    canvas.grid(row=0, column=0, sticky="nsew", columnspan=9)
    scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=10, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    inner_frame = Frame(canvas, highlightbackground="red", highlightthickness=2)
    # inner_frame.grid()
    canvas.create_window((0,0), window=inner_frame, anchor="nw")
    # Add 9-by-5 buttons to the frame
    system_fonts = families()
    count = 0
    rows = int(len(system_fonts)/2)
    columns = 2
    labels = [[tk.Button() for j in range(columns)] for i in range(rows)]
    labels = [[Label() for j in range(columns)] for i in range(rows)]
    print(len(labels))
    for i in range(0, rows):
        # for j in range(0, columns):
      font_family =  system_fonts[count]
      count += 1
      labels[i][0] = Label(inner_frame, text=font_family, font=label_font)
      labels[i][0].grid(row=i, column=0, sticky="nsew")
      labels[i][1] = Label(inner_frame, text=font_family, font=(font_family, 12))
      labels[i][1].grid(row=i, column=1, sticky="nsew")
            # buttons[i][j] = tk.Button(inner_frame, text=system_fonts[i])
            # buttons[i][j].grid(row=i, column=j, sticky='news')
    inner_frame.update_idletasks()
    first5columns_width = sum([labels[0][j].winfo_width() for j in range(0, 2)])
    first5rows_height = sum([labels[i][0].winfo_height() for i in range(0, 15)])
    print(first5columns_width, first5rows_height)
    frame.config(width=first5columns_width + scrollbar.winfo_width(),
                        height=first5rows_height)
    
    # Set the canvas scrolling region
    canvas.config(scrollregion=canvas.bbox("all"))