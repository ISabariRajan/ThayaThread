from PIL import ImageTk


class GUIOperations:

  def load_imagetk(self, image_path):
    return ImageTk.PhotoImage(image_path)

  def load_logo(self):
    pass