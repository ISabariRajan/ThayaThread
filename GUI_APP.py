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
from GUI.Frame.Operation import GUIOperationFrame
from GUI.Frame.Image import ImageFrame
from GUI.Frame.Controls import ControlFrame
from GUI.Functions.guifunctions import GUIFunctions
from json import loads, dumps
from types import SimpleNamespace
from GUI.globals import shared_object
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
    self.functions = GUIFunctions()

  
  def create_skeleton(self):
    self.WIDGET.geometry("2000x1000+2800+100")
    self.WIDGET.grid_columnconfigure(0, weight=1)

    heading_frame = Frame(self.WIDGET, highlightbackground="black", highlightthickness=3)
    heading_frame.grid(row=0, column=0, columnspan=2000, sticky="nsew")

    l1 = Label(heading_frame, text="Thaya Thread Softwares", font=self.config.heading_font)
    l1.grid(row=0, column=0)
    l1.pack()
    self.create_selection_frame()

  def create_selection_frame(self):
    selection_frame = Frame(self.WIDGET, highlightbackground="black", highlightthickness=3)
    selection_frame.grid(row=1, column=0, columnspan=20, sticky="nswe")

    options = [
      "T1", "T2"
    ]
    option_values = StringVar(name="app_selection")
    option_values.set("---SELECT---")
    Label(selection_frame, text="Select").grid(row=0, column=0)
    OptionMenu(selection_frame, option_values, *options).grid(row=0, column=1)
    option_values.trace_add("write", self.load_frame)
    self.load_option = option_values

  def clear_frame(self):
    for x in self.running_frame.winfo_children():
      x.destroy()

  def load_frame(self, *kwargs):
    print(kwargs, self.load_option.get())
    option = self.load_option.get()
    self.running_frame = Frame(self.WIDGET, highlightbackground="blue", highlightthickness=2)
    self.running_frame.grid(row=2, column=0, columnspan=10, sticky="nwes")
    self.running_frame.columnconfigure(0, weight=1)
    
    if option == "T1":
      self.generate_frame(self.running_frame)

  def generate_frame(self, root):
      # frame.generate_frame(self.running_frame)
    frame = Frame(root, highlightbackground="red", highlightthickness=3)
    frame.columnconfigure(0, weight=5)
    frame.columnconfigure(5, weight=5)
    frame.grid(row=0, column=0, sticky="nsew")
    img_frame = ImageFrame()
    gui_operation_frame = GUIOperationFrame()
    img_frame.generate_frame(frame)
    gui_operation_frame.generate_frame(frame)
    # root.update()
    # inner_frame_width = int(frame.winfo_width()/2)




    # left_frame.pack()
    right_frame = Frame(frame, highlightbackground="green", highlightthickness=2, height=600)
    right_frame.grid(row=0, column=5, sticky="nsew", columnspan=5)
    control_frame = ControlFrame()
    control_frame.generate_frame(right_frame)
    # right_frame.grid_propagate(False)

    # update_button = tk.Button(frame, text="Download", command=lambda: self.download())
    # update_button.grid(row=2, column=1, padx=50, pady=30)

    # exit_button = tk.Button(frame, text="Exit", command=lambda: self.download())
    # exit_button.grid(row=2, column=2, padx=50, pady=30)
    # self.root.pack()
    # frame.pack()

  def download(self):
    pass



  def run(self):
    self.WIDGET.mainloop()

app = APP()
app.create_skeleton()
app.run()

# obj = ImageFrame()
# obj.input_folder = Path(r"E:\Reorganized\Works\Sabari\ThayaThread\VideoGenerator\Input")
# obj.output_folder = Path(r"E:\Reorganized\Works\Sabari\ThayaThread\VideoGenerator\Output")
# obj.get_input_folder()