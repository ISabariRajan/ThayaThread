import tkinter as tk
from tkinter import Tk, Frame, StringVar, Label, OptionMenu, LabelFrame
from tkinter import messagebox, filedialog
from pathlib import Path
from os import listdir
from os.path import join as joinpath, dirname
from tkinter import filedialog
from VideoGenerator.guioperations import GUIOperations
from VideoGenerator.videogenerator import VideoGenerator
from guifunctions import GUIFunctions
from VideoGenerator.image_operations import list_images_in_folder, resize_image_by_width, \
  draw_overlay, open_rgba_image, new_layer, create_text_image, add_fill_background
from PIL import ImageTk

from json import loads, dumps
from types import SimpleNamespace

cur_dir = dirname(__file__)

class Config:
  config = {
    "heading_font": ("Helvetica", 30)
  }
  def __init__(self) -> None:
    self.config = loads(dumps(self.config), object_hook=lambda d: SimpleNamespace(**d))


class APP:

  WIDGET = object()
  config = Config().config
  def __init__(self) -> None:
    self.WIDGET = Tk(screenName="Thaya thread")
    self.WIDGET.title("Test")

  
  def create_skeleton(self):
    self.WIDGET.geometry("1000x1000+1000+100")
    # self.WIDGET.
    self.WIDGET.grid_columnconfigure(0, weight=1)
    # # self.WIDGET.grid_columnconfigure(0, weight=1)
    # self.WIDGET.grid_rowconfigure(0, weight=0)


    heading_frame = Frame(self.WIDGET, highlightbackground="black", highlightthickness=3)
    heading_frame.grid(row=0, column=0, columnspan=2000, sticky="nsew")

    l1 = Label(heading_frame, text="Thaya Thread Softwares", font=self.config.heading_font)
    l1.grid(row=0, column=0)
    l1.pack()
    self.create_selection_frame()
    # self.WIDGET.pack()

  def create_selection_frame(self):
    selection_frame = Frame(self.WIDGET, highlightbackground="black", highlightthickness=3)
    selection_frame.grid(row=1, column=0, columnspan=20, sticky="nswe")
    # selection_frame.pack()

    options = [
      "T1", "T2"
    ]
    option_values = StringVar(name="app_selection")
    option_values.set("---SELECT---")
    Label(selection_frame, text="Select").grid(row=0, column=0)
    OptionMenu(selection_frame, option_values, *options).grid(row=0, column=1)
    option_values.trace_add("write", self.load_frame)
    self.load_option = option_values
    # option_values.trace_add("read", self.load_frame)

  def clear_frame(self):
    for x in self.running_frame.winfo_children():
      x.destroy()

  def load_frame(self, *kwargs):
    print(kwargs, self.load_option.get())
    option = self.load_option.get()
    self.running_frame = Frame(self.WIDGET, highlightbackground="blue", highlightthickness=2)
    self.running_frame.grid(row=2, column=0, columnspan=10, sticky="nwe")
    self.running_frame.columnconfigure(0, weight=1)
    
    if option == "T1":
      frame = ImageFrame()
      frame.generate_frame(self.running_frame)

  def run(self):
    self.WIDGET.mainloop()

class ImageFrame:

  def __init__(self) -> None:
    self.operations = GUIOperations()
    self.font_config = {
        "name": "arial.ttf",
        "size": 100
      }
    self.logo_folder = Path(joinpath(cur_dir, "VideoGenerator", "assets", "logo"))

  def generate_frame(self, root):

    logo_path = Path(joinpath(self.logo_folder, "thaya-thread-logo-crop.png"))

    frame = Frame(root, highlightbackground="red", highlightthickness=3)
    frame.columnconfigure(0, weight=5)
    frame.columnconfigure(5, weight=5)
    frame.grid(row=0, column=0, sticky="nsew")
    root.update()
    inner_frame_width = int(frame.winfo_width()/2)

    left_frame = Frame(frame, highlightbackground="green", highlightthickness=2, width=inner_frame_width, height=600)
    left_frame.grid(row=0, column=0, sticky="nsew", columnspan=5)
    # left_frame.grid_propagate(False)
    Label(left_frame, text="Original", font=("Helvetica", 24), highlightbackground="blue", highlightthickness=2).grid(row=0, column=0)

    # left_frame.pack()
    right_frame = Frame(frame, highlightbackground="green", highlightthickness=2, width=inner_frame_width, height=600)
    right_frame.grid(row=0, column=5, sticky="nsew", columnspan=5)
    # right_frame.grid_propagate(False)
    Label(right_frame, text="Updated", font=("Helvetica", 24), highlightbackground="red", highlightthickness=2).grid(row=0, column=0)

    # right_frame.pack()

    print(cur_dir)
    image_canvas_1 = tk.Canvas(left_frame, highlightbackground="blue", highlightthickness=2, height=600, width=400)
    image_canvas_1.grid(row=1, column=0, padx=30, sticky="n")
    self.orig = ImageTk.PhotoImage(file=str(logo_path))
    image_canvas_1.create_image((0, 0), image=self.orig, anchor="nw")
    self.canvas1 = image_canvas_1

    image_canvas_2 = tk.Canvas(right_frame, highlightbackground="blue", highlightthickness=2, height=600, width=400)
    image_canvas_2.grid(row=1, column=0, padx=30, sticky="n")
    self.updated = ImageTk.PhotoImage(file=str(logo_path))
    image_canvas_2.create_image((0, 0), image=self.updated, anchor="nw")
    self.canvas2 = image_canvas_2

    select_folder_button = tk.Button(frame, text="Select Input Folder", command=lambda: self.get_input_folder())
    select_folder_button.grid(row=2, column=0, padx=50, pady=30)

    # update_button = tk.Button(frame, text="Download", command=lambda: self.download())
    # update_button.grid(row=2, column=1, padx=50, pady=30)

    # exit_button = tk.Button(frame, text="Exit", command=lambda: self.download())
    # exit_button.grid(row=2, column=2, padx=50, pady=30)
    # self.root.pack()
    # frame.pack()


  def download(self):
    pass


  def get_input_folder(self):
    self.input_folder = filedialog.askdirectory(title="Input Folder")
    self.output_folder = filedialog.askdirectory(title="Output Folder")
    
    image_name = list_images_in_folder(self.input_folder)
    img_path = Path(joinpath(self.input_folder, image_name[0]))
    img = open_rgba_image(img_path)
    img = resize_image_by_width(img, 400).convert("RGB")
    img_path = Path(joinpath(self.output_folder, image_name[0]))
    img.save(img_path)
    self.orig = ImageTk.PhotoImage(file=str(img_path))
    self.canvas1.create_image((0, 0), image=self.orig, anchor="nw")

    # Update contact
    img_path = Path(joinpath(self.input_folder, image_name[0]))
    updated_image = open_rgba_image(img_path)
    updated_image = self.add_logo_to_image(updated_image)
    updated_image = self.add_whatsapp_contact_to_image(updated_image)
    img_path = Path(joinpath(self.output_folder, "updated-" + image_name[0]))
    updated_image = resize_image_by_width(updated_image, 400).convert("RGB")
    updated_image.save(img_path)
    self.updated = ImageTk.PhotoImage(file=str(img_path))
    self.canvas2.create_image((0, 0), image=self.updated, anchor="nw")


  def load_imagetk(self):
    return self.functions.load_imagetk()
  
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



app = APP()
app.create_skeleton()
app.run()

# obj = ImageFrame()
# obj.input_folder = Path(r"E:\Reorganized\Works\Sabari\ThayaThread\VideoGenerator\Input")
# obj.output_folder = Path(r"E:\Reorganized\Works\Sabari\ThayaThread\VideoGenerator\Output")
# obj.get_input_folder()