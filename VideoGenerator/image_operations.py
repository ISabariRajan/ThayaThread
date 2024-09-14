from PIL import Image, ImageDraw, ImageFont
from os.path import join as joinpath
from os import listdir
import cv2
import numpy as np

transparent_color = (255, 255, 255, 0)

def load_ImageTk(image_path):
  pass

def list_images_in_folder(input_folder):
  valid_images = []
  for curr_file in listdir(input_folder):
    if curr_file.lower().endswith((".jpeg", ".jpg", ".png")):
        valid_images.append(curr_file)
  return valid_images

def get_avg_image_size(folder_name, image_list):
  total_width = 0
  total_height = 0
  total_images = 0
  for curr_file in image_list:
    curr_file = joinpath(folder_name, curr_file)
    image = Image.open(curr_file)
    w, h = image.size
    total_height += h
    total_width += w
    total_images += 1

  avg_width = int(total_width/total_images)
  avg_height = int(total_height/total_images)
  return avg_width, avg_height

def to_rgba(img):
  if img.mode != "RGBA":
    return img.convert("RGBA")
  return img

def to_rgb(img):
  if img.mode != "RGB":
    return img.convert("RGB")
  return img

def draw_rectange_over_image(
      image,
      rect_axis = [10, 10, 110, 120],
      fill_color = (0, 0, 255),
      outline_color = (0, 0, 255),
      border_width = 2,
      border_radius = 300,
      is_png = True
    ):
  if is_png:
    img_type = "RGBA"  
  else:
    img_type = "RGB"
  rect_img = Image.new(img_type, image.size, (255, 255, 255, 0))
  draw = ImageDraw.Draw(rect_img)
  if border_radius:
    draw.rounded_rectangle(
      rect_axis,
      fill=fill_color,
      outline=outline_color,
      width=3,
      radius=border_radius
    )
  else:
    draw.rectangle(
      rect_axis,
      fill=fill_color,
      outline=outline_color,
      width=border_width
    )
  return Image.alpha_composite(image, rect_img)

def create_text_image(
    text,
    font_config,
    fill_color=(0, 0, 255)
):
  img = Image.new("RGBA", (2000,2000), transparent_color)
  draw_obj = ImageDraw.Draw(img)
  font = ImageFont.truetype(font_config["name"], size=font_config["size"])
  draw_obj.text((0, 0), text=text, font=font, fill=fill_color)
  bbox = font.getbbox(text)
  img = img.crop(bbox)
  return img

def draw_overlay(
    bg_image,
    fg_image,
    fg_image_axis,
    fg_image_resize=None,
    fg_image_preserve_ar=True
  ):
  fg_image = to_rgba(fg_image)
  bg_image = to_rgba(bg_image)
  if fg_image_resize:
    fg_image = resize_image(fg_image, fg_image_resize, fg_image_preserve_ar)
  new_fg_image = Image.new("RGBA", bg_image.size)
  new_fg_image.paste(fg_image, fg_image_axis, fg_image)
  bg_image.paste(new_fg_image, (0,0), mask=new_fg_image)
  return Image.alpha_composite(bg_image, new_fg_image)

def resize_image_by_width(
      img,
      resize_width
  ):

  scale_factor = resize_width/img.width
  img_re_size = (int(img.width * scale_factor), int(img.height * scale_factor))
  return resize_image(img, img_re_size, preserve_aspect_ratio=True)

def draw_text_to_image(
      img,
      text,
      font_config,
      axis,
      fill_color = (255,0,0),
      text_width=None
    ):
    text_img = create_text_image(text, font_config, fill_color)
    if text_width:
      scale_factor = text_width/text_img.width
      text_img_resize = (int(text_img.width * scale_factor), int(text_img.height * scale_factor))
    else:
      text_img_resize = None

    img = draw_overlay(img, text_img,axis, fg_image_resize=text_img_resize)
    img.save("output.png")
    return img


def get_rgba_image(image_path):
  return Image.open(image_path).convert("RGBA")

def resize_image(img, new_size, preserve_aspect_ratio=False):
  if(preserve_aspect_ratio):
    width, height = img.size
    w1, h1 = new_size
    scale_factor = min(w1/width, h1,height)
    return img.resize((int(scale_factor * width), int(scale_factor * height)), Image.Resampling.LANCZOS)
  return img.resize(new_size)

def add_image_overlay(background_image_path, foreground_image_path):
  background_image = get_rgba_image(background_image_path)
  foreground_image = get_rgba_image(foreground_image_path)
  foreground_image = resize_image(foreground_image_path, (100, 100), preserve_aspect_ratio=True)
  new_foreground_image = Image.new("RGBA", background_image.size)
  new_foreground_image.paste(foreground_image, (0,0), foreground_image)
  background_image.paste(new_foreground_image, (0,0), mask=new_foreground_image)
  return Image.alpha_composite(background_image, new_foreground_image).convert("RGB")