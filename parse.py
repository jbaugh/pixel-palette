import os, sys
from PIL import Image

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
    print(color + ":" + str(pixels[color]))

def generate_image(pixels):
  cv2.imwrite("output/test.png", [pixels.values()])

pixels = get_pixels('samples/sprite1.png')
print_pixels(pixels)
# generate_image(pixels)

