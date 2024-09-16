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

class GUIFunctions:
  def add_logo_to_image(self, img):
    logo_path = joinpath(self.logo_folder, "thaya-thread-logo-crop.png")
    logo_img = open_rgba_image(logo_path)
    logo_img = add_fill_background(logo_img, (255, 255, 255, 200))
    logo_axis = (
      (int (img.width/2) - int(logo_img.width/2)),
      (int (img.height/2) - int(logo_img.height/2))
    )
    print(logo_axis)
    return draw_overlay(
      img,
      logo_img,
      logo_axis
    )

  def add_whatsapp_contact_to_image(self, img):
    whatsapp_image = self.create_whatsapp_contact_image("+91-8015399392")
    whatsapp_image.save("output.png")
    whatsapp_image_axis = (
        (img.width - 30 - whatsapp_image.width),
        30
      )
    return draw_overlay(
      img,
      whatsapp_image,
      whatsapp_image_axis
    )

  def create_whatsapp_contact_image(self, contact_number):
    logo_path = joinpath(self.logo_folder, "whatsapp-logo.png")
    whatsapp_image = open_rgba_image(str(logo_path))
    bg_image = new_layer((0,0,0,100))
    bg_image = draw_overlay(bg_image, whatsapp_image, (0, 0), (100, 100))
    phone_number = create_text_image(contact_number, self.font_config)
    phone_number = resize_image_by_width(phone_number, 500)
    total_width = phone_number.width + 100
    bg_image = draw_overlay(bg_image, phone_number, (100, 30))
    bg_image.save("output.png")
    return bg_image.crop((0, 0, total_width, 100))

