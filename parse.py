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
  color = [hex_code[i:i+2] for i in range(0, len(hex_code), 2)]
  return [int(color[0], 16), int(color[1], 16), int(color[2], 16), int(color[3], 16)]

def get_color(colors, square_size, num_colors_col, x, y):
  xindex = x // square_size
  yindex = y // square_size
  color_index = xindex + (yindex * num_colors_col)


  if color_index >= len(colors):
    return [255, 255, 255, 255]
  else:
    return hex_to_pixel(colors[color_index])

def generate_image(pixels):
  square_size = 10
  num_colors_col = 10
  image_size = square_size * num_colors_col
  colors = list(pixels)
  arr = []

  for y in range(image_size):
    row = []
    for x in range(image_size):
      row.append(get_color(colors, square_size, num_colors_col, x, y))
    arr.append(row)

  array = numpy.array(arr, dtype=numpy.uint8)
  img = Image.fromarray(array)
  img.save('output/test.png')


pixels = get_pixels('samples/sprite1.png')
print_pixels(pixels)
generate_image(pixels)

