from tkinter import Label
from VideoGenerator.image_operations import new_layer, resize_image_by_width

class SharedObject:
  canvas1 = canvas2 = ""
  logo_image = whatsapp_logo_image = new_layer(fill_color=(255, 255, 255, 255))
  orig_image = updated_image = new_layer(fill_color=(255, 255, 255, 255))
  orig = updated = None
  total_images = ""
  end_series_number = ""
  starting_series_number = ""
  series_prefix = ""
  whatsapp_contact_number = ""
  def __init__(self) -> None:
    self.logo_image = resize_image_by_width(self.logo_image, 100)
    
shared_object = SharedObject()

heading_font = ("Helvetica", 16)
label_font = ("Helvetica", 8)
font_config = {
    "name": "arial.ttf",
    "size": 100
  }

def create_heading_label(frame, text):
  Label(frame, text=text, font=heading_font, highlightbackground="blue", highlightthickness=2).grid(row=0, column=0, sticky="nsew", padx=30, columnspan=3, pady=50)