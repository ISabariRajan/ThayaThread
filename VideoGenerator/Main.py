import os
import cv2
import numpy as np
from os import listdir
from math import floor
from PIL import Image, ImageDraw, ImageFont
from os.path import dirname, join as joinpath
from cv2 import imread, imshow, VideoWriter, VideoWriter_fourcc

from video_generator import add_image_overlay, draw_text_to_image,\
    list_images_in_folder, draw_rectange_over_image, draw_overlay, transparent_color,\
    create_text_image, resize_image_by_width

curr_dir = dirname(__file__)
input_folder = joinpath(curr_dir, "Input")
output_folder = joinpath(curr_dir, "Output")
overlay_image_path = joinpath(curr_dir, "logo.png")


class VideoGenerator:

  total_duration_seconds = 30
  start_duration_seconds = 2
  end_duration_seconds = 0
  mid_duration_seconds = 26
  format = "H.264"
  FPS = 25
  video_filename = "output.mp4"

  def __init__(self, input_folder) -> None:
    self.input_folder = input_folder
    self.valid_images = list_images_in_folder(input_folder)
    self.no_of_images = len(self.valid_images)
    width, height = self.get_average_size_of_images()
    self.average_size = (width, height)

    self.mid_frames_per_image = self.frames_per_image(self.mid_duration_seconds)
    self.start_frames_per_image = self.frames_per_image(self.start_duration_seconds)

    total_frames = self.total_duration_seconds * self.FPS
    self.start_duration_frames = self.start_frames_per_image * self.no_of_images
    self.mid_duration_frames = self.mid_frames_per_image * self.no_of_images
    self.end_duration_frames = total_frames - self.start_duration_frames - self.mid_duration_frames
    
    padding = 30
    self.rect_axis = [padding, padding, self.average_size[0] - padding, self.average_size[1] - padding]
    mid_width, mid_height = (int(width/2), int(height/2))
    self.text_axis = {
      "start": (padding * 2, mid_height)
    }
    self.font_config = {
        "name": "arial.ttf",
        "size": 100
      }
    self.padding = padding


  def get_average_size_of_images(self):
    total_width = 0
    total_height = 0
    total_images = 0
    for curr_file in self.valid_images:
      curr_file = joinpath(self.input_folder, curr_file)
      image = Image.open(curr_file)
      w, h = image.size
      total_height += h
      total_width += w
      total_images += 1

    avg_width = int(total_width/total_images)
    avg_height = int(total_height/total_images)
    return avg_width, avg_height

  def resize_images(
        self,
        input_folder_path,
        output_folder_path
      ):
    for image_file in self.valid_images:
      img = Image.open(joinpath(input_folder_path, image_file))
      img = img.resize(self.average_size)
      img.save(joinpath(output_folder_path, image_file), "JPEG", quality=95)
    pass

  def frames_per_image(self, total_duration):
    return floor(total_duration * self.FPS / self.no_of_images)

  def create_whatsapp_contact_image(self, contact_number):
    whatsapp_image = Image.open("assets/logo/whatsapp-logo.png")
    bg_image = Image.new("RGBA", (2000, 2000), transparent_color)
    bg_image = draw_overlay(bg_image, whatsapp_image, (0, 0), (100, 100))
    phone_number = create_text_image(contact_number, self.font_config)
    phone_number = resize_image_by_width(phone_number, 500)
    total_width = phone_number.width + 100
    bg_image = draw_overlay(bg_image, phone_number, (100, 30))
    bg_image.save("output.png")
    return bg_image.crop((0, 0, total_width, 100))


  def create_video_writer(self):
    codec = VideoWriter_fourcc(*'mp4v')
    self.writer = cv2.VideoWriter(self.video_filename, codec, self.FPS, self.average_size) 

  def release_video_writer(self):
    self.writer.release()

  def generate_start_video(self, images_folder):
    self.writer
    for image_path in self.valid_images:
      image_path = joinpath(images_folder, image_path)
      loaded_img = Image.open(image_path).convert("RGBA")

      # Draw outer rectange
      loaded_img = draw_rectange_over_image(
          loaded_img,
          rect_axis=self.rect_axis,
          fill_color = (255, 0 ,0, 0),
          border_radius=15
        )
      
      # Draw Saree text
      width = self.average_size[0] - (self.padding * 4)
      loaded_img = draw_text_to_image(
          loaded_img,
          "Kaancheepuram Sarees".upper(),
          font_config=self.font_config,
          axis=self.text_axis["start"],
          fill_color=(0,0,255),
          text_width=width
        )
      loaded_img = cv2.cvtColor(np.array(loaded_img), cv2.COLOR_RGB2BGR)
      for _ in range(self.start_frames_per_image):
        self.writer.write(loaded_img)

  def genearte_mid_video(self, images_folder):
    whatsapp_contact_image = self.create_whatsapp_contact_image("+91-8015399392")
    whatsapp_image_axis = (
        (self.average_size[0] - self.padding - whatsapp_contact_image.width),
        self.padding
      )
    for image_path in self.valid_images:
      image_path = joinpath(images_folder, image_path)
      loaded_img = Image.open(image_path).convert("RGBA")
      loaded_img = draw_overlay(
        loaded_img,
        whatsapp_contact_image,
        whatsapp_image_axis
      )
      loaded_img.save("output.png")
      loaded_img = cv2.cvtColor(np.array(loaded_img), cv2.COLOR_RGB2BGR)
      for _ in range(self.mid_frames_per_image):
        self.writer.write(loaded_img)

  def generate_end_video(self, images_folder):
    pass
    # for image_path in self.valid_images:
    #   image_path = joinpath(images_folder, image_path)
    #   loaded_img = cv2.imread(image_path)
    #   for _ in range(self.end_duration_frames):
    #     self.writer.write(loaded_img)

  def create_video(self, images_folder):
    self.create_video_writer()
    self.generate_start_video(images_folder)
    self.genearte_mid_video(images_folder)
    self.generate_end_video(images_folder)
    self.release_video_writer()

  def run(self):
    self.resize_images(input_folder, output_folder)
    self.create_video(output_folder)

obj = VideoGenerator(input_folder)
obj.run()