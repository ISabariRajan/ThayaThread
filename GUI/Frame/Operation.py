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
from GUI.Functions.guifunctions import GUIFunctions
from GUI.globals import shared_object
from json import loads, dumps
from types import SimpleNamespace

class GUIOperationFrame:

  def __init__(self) -> None:
    self.functions = GUIFunctions()
    self.obj = shared_object

  def generate_frame(self, root):
    frame = Frame(root)
    frame.grid(row=1, column=0, sticky="nsew", columnspan=5)

    self.input_folder = StringVar(value="Input Folder")
    Label(frame, text="Input Folder", font=("Helvetica", 16), highlightbackground="blue", highlightthickness=2).grid(row=0, column=0, sticky="e", padx=30)
    self.input_folder_text = Entry(frame, textvariable=self.input_folder, font=("Helvetica", 16), highlightbackground="blue", highlightthickness=2, state="disabled")
    self.input_folder_text.grid(row=0, column=1, sticky="e")
    input_folder_button = tk.Button(frame, text="Browse", command=lambda: self.get_input_folder())
    input_folder_button.grid(row=0, column=2, sticky="w")

    self.output_folder = StringVar(value="Output Folder")
    Label(frame, text="Output Folder", font=("Helvetica", 16), highlightbackground="blue", highlightthickness=2).grid(row=1, column=0, sticky="e", padx=30)
    self.output_folder_text = Entry(frame, textvariable=self.output_folder, font=("Helvetica", 16), highlightbackground="blue", highlightthickness=2, state="disabled")
    self.output_folder_text.grid(row=1, column=1, sticky="e")
    output_folder_button = tk.Button(frame, text="Browse", command=lambda: self.get_output_folder())
    output_folder_button.grid(row=1, column=2, sticky="w")
    
    update_image = tk.Button(frame, text="Update Image", command=lambda: self.update_image())
    update_image.grid(row=2, column=0, padx=50, pady=30)

  def get_output_folder(self):
    output_folder = filedialog.askdirectory(title="Output Folder")
    self.output_folder.set(Path(output_folder))
    self.output_folder_text.insert(0, self.output_folder.get())

  def get_input_folder(self):
    input_folder = filedialog.askdirectory(title="Input Folder")
    self.input_folder.set(Path(input_folder))    
    self.input_folder_text.insert(0, self.input_folder.get())

  def update_image(self):    
    image_name = list_images_in_folder(self.input_folder.get())
    img_path = Path(joinpath(self.input_folder.get(), image_name[0]))
    img = open_rgba_image(img_path)
    img = resize_image_by_width(img, 400).convert("RGB")
    img_path = Path(joinpath(self.output_folder.get(), image_name[0]))
    img.save(img_path)
    self.orig = ImageTk.PhotoImage(file=str(img_path))
    self.obj.canvas1.create_image((0, 0), image=self.orig, anchor="nw")

    # Update contact
    img_path = Path(joinpath(self.input_folder.get(), image_name[0]))
    updated_image = open_rgba_image(img_path)
    updated_image = self.functions.add_logo_to_image(updated_image, self.obj.logo_image)
    updated_image = self.functions.add_whatsapp_contact_to_image(updated_image, self.obj.whatsapp_logo_image)
    img_path = Path(joinpath(self.output_folder.get(), "updated-" + image_name[0]))
    updated_image = resize_image_by_width(updated_image, 400).convert("RGB")
    updated_image.save(img_path)
    self.updated = ImageTk.PhotoImage(file=str(img_path))
    self.obj.canvas2.create_image((0, 0), image=self.updated, anchor="nw")
