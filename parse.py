import os, sys
from PIL import Image
import numpy

def hex_chunk(num):
  s = str(hex(num)).replace('0x', '')
  if len(s) == 1:
    s = '0' + s
  return s


def pixel_to_rgba(pixel):
  return hex_chunk(pixel[0]) + hex_chunk(pixel[1]) + hex_chunk(pixel[2]) + hex_chunk(pixel[3])


def get_pixels(fpath, ignore_colors = [], ignore_invisible = True):
  pixels = {}
  with Image.open(fpath) as im:
    for i in range(1, im.size[0]):
      for j in range(1, im.size[1]):
        pixel = im.getpixel((i, j))

        # If ignore_invisible is True, ignore pixels with alpha of 0 (i.e. invisible)
        if not ignore_invisible or pixel[3] != 0:
          hex_pixel = pixel_to_rgba(pixel)
          if hex_pixel not in ignore_colors:
            if hex_pixel in pixels:
              pixels[hex_pixel] += 1
            else:
              pixels[hex_pixel] = 1

  # Sort the pixels
  return {k: v for k, v in reversed(sorted(pixels.items(), key=lambda item: item[1]))}


def print_pixels(pixels):
  for color in pixels:
    print(color + ':' + str(pixels[color]))

def hex_to_pixel(hex_code):
  return [35, 110, 31, 255]

def generate_image(pixels):
  color_left = 1
  color_right = 10
  color_top = 1
  color_bottom = 10
  color_size = 10
  padding = 1
  colors = list(pixels)
  color = hex_to_pixel(colors[0])
  arr = []
  blank_color = [255, 255, 255, 255]

  for y in range(101):
    row = []
    for x in range(101):
      if x >= color_left and x <= color_right:
        if y >= color_top and y <= color_bottom:
          row.append(color)
        else:
          row.append(blank_color)
          if len(colors) > 1:
            colors.pop(0)
            color = hex_to_pixel(colors[0])
          else:
            color = blank_color
      else:
        row.append(blank_color)

    arr.append(row)

  array = numpy.array(arr, dtype=numpy.uint8)
  img = Image.fromarray(array)
  img.save('output/test.png')


pixels = get_pixels('samples/sprite1.png')
print_pixels(pixels)
generate_image(pixels)

