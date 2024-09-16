import tkinter as tk
from tkinter import Tk, Frame, StringVar, Label, OptionMenu, LabelFrame, Entry
from tkinter import messagebox, filedialog
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
cur_dir = dirname(__file__)
class ImageFrame:

  def __init__(self) -> None:
    self.operations = GUIOperations()
    self.font_config = {
        "name": "arial.ttf",
        "size": 100
      }
    self.logo_folder = Path(joinpath(cur_dir, "VideoGenerator", "assets", "logo"))

  def generate_frame(self, root):
    
    frame = Frame(root, highlightbackground="green", highlightthickness=2, height=600)
    frame.grid(row=0, column=0, sticky="nsew", columnspan=5)

    Label(frame, text="Original", font=("Helvetica", 24), highlightbackground="blue", highlightthickness=2).grid(row=0, column=0)
    Label(frame, text="Updated", font=("Helvetica", 24), highlightbackground="red", highlightthickness=2).grid(row=0, column=1)

    logo_path = Path(joinpath(self.logo_folder, "thaya-thread-logo-crop.png"))
    print(cur_dir)
    img = new_layer(fill_color=(255, 255, 255, 255))
    image_canvas_1 = tk.Canvas(frame, highlightbackground="blue", highlightthickness=2, height=600, width=400)
    image_canvas_1.grid(row=1, column=0, padx=30, sticky="n")
    self.orig = ImageTk.PhotoImage(img)
    # self.orig - tk.PhotoImage(image=img)
    image_canvas_1.create_image((0, 0), image=self.orig, anchor="nw")
    self.canvas1 = image_canvas_1

    image_canvas_2 = tk.Canvas(frame, highlightbackground="blue", highlightthickness=2, height=600, width=400)
    image_canvas_2.grid(row=1, column=1, padx=30, sticky="n")
    self.updated = ImageTk.PhotoImage(img)
    # self.updated - tk.PhotoImage(image=img)
    image_canvas_2.create_image((0, 0), image=self.updated, anchor="nw")
    self.canvas2 = image_canvas_2
