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
from GUI.globals import shared_object, create_heading_label, label_font

class ControlFrame():
  
  obj = shared_object

  def generate_frame(self, root):
    frame = Frame(root)
    frame.grid(row=2, column=0, sticky="nsew", columnspan=5)
    create_heading_label(frame, "Controls")

    self.logo_path = StringVar(value="Logo Path")
    Label(frame, text="Logo path", font=label_font, highlightbackground="blue", highlightthickness=2).grid(row=1, column=0, sticky="e", padx=30)
    self.logo_path_text = Entry(frame, textvariable=self.logo_path, font=label_font, highlightbackground="blue", highlightthickness=2, state="disabled")
    self.logo_path_text.grid(row=1, column=1, sticky="e")
    logo_path_button = tk.Button(frame, text="Browse", command=lambda: self.get_logo_path())
    logo_path_button.grid(row=1, column=2, sticky="w")

    self.whatsapp_logo_path = StringVar(value="Whatsapp Logo Path")
    Label(frame, text="Whatsapp Logo path", font=label_font, highlightbackground="blue", highlightthickness=2).grid(row=2, column=0, sticky="e", padx=30)
    self.whatsapp_logo_path_text = Entry(frame, textvariable=self.whatsapp_logo_path, font=label_font, highlightbackground="blue", highlightthickness=2, state="disabled")
    self.whatsapp_logo_path_text.grid(row=2, column=1, sticky="e")
    whatsapp_logo_path_button = tk.Button(frame, text="Browse", command=lambda: self.get_whatsapp_logo_path())
    whatsapp_logo_path_button.grid(row=2, column=2, sticky="w")

    self.obj.whatsapp_contact_number = StringVar(value="+91-8015399392")
    Label(frame, text="Whatsapp Contact Number", font=label_font, highlightbackground="blue", highlightthickness=2).grid(row=3, column=0, sticky="e", padx=30)
    self.whatsapp_contact_number_text = Entry(frame, textvariable=self.obj.whatsapp_contact_number, font=label_font, highlightbackground="blue", highlightthickness=2)
    self.whatsapp_contact_number_text.grid(row=3, column=1, sticky="we", columnspan=2)

    self.obj.series_prefix = StringVar(value="KB")
    Label(frame, text="Series Prefix", font=label_font, highlightbackground="blue", highlightthickness=2).grid(row=4, column=0, sticky="e", padx=30)
    self.series_prefix_text = Entry(frame, textvariable=self.obj.series_prefix, font=label_font, highlightbackground="blue", highlightthickness=2)
    self.series_prefix_text.grid(row=4, column=1, sticky="we", columnspan=2)

    self.obj.starting_series_number = StringVar(value="000000")
    Label(frame, text="Series start number", font=label_font, highlightbackground="blue", highlightthickness=2).grid(row=5, column=0, sticky="e", padx=30)
    self.starting_series_number_text = Entry(frame, textvariable=self.obj.starting_series_number, font=label_font, highlightbackground="blue", highlightthickness=2)
    self.starting_series_number_text.grid(row=5, column=1, sticky="we", columnspan=2)
  
    self.obj.total_images = StringVar(value="0")
    Label(frame, text="Total Images: ", font=label_font, highlightbackground="blue", highlightthickness=2).grid(row=6, column=0, sticky="e", padx=30)
    self.total_images_text = Entry(frame, textvariable=self.obj.total_images, font=label_font, highlightbackground="blue", highlightthickness=2, state="disabled")
    self.total_images_text.grid(row=6, column=1, sticky="we", columnspan=2)

    self.obj.end_series_number = StringVar(value="0")
    Label(frame, text="End Series Number: ", font=label_font, highlightbackground="blue", highlightthickness=2).grid(row=7, column=0, sticky="e", padx=30)
    self.end_series_number_text = Entry(frame, textvariable=self.obj.end_series_number, font=label_font, highlightbackground="blue", highlightthickness=2, state="disabled")
    self.end_series_number_text.grid(row=7, column=1, sticky="we", columnspan=2)


  def get_logo_path(self):
    logo_path = filedialog.askopenfilename(title="Logo Path")
    logo_path = Path(logo_path)
    self.logo_path.set(logo_path)
    self.logo_path_text.insert(0, self.logo_path.get())
    self.obj.logo_image = open_rgba_image(logo_path)

  def get_whatsapp_logo_path(self):
    whatsapp_logo_path = filedialog.askopenfilename(title="Whatsapp Logo Path")
    whatsapp_logo_path = Path(whatsapp_logo_path)
    self.whatsapp_logo_path.set(whatsapp_logo_path)
    self.whatsapp_logo_path_text.insert(0, self.whatsapp_logo_path.get())
    self.obj.whatsapp_logo_image = open_rgba_image(whatsapp_logo_path)
