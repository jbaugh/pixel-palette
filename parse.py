import cv2

def hex_chunk(num):
  s = str(hex(num)).replace('0x', '')
  if len(s) == 1:
    s = '0' + s
  return s

def pixel_to_rgba(pixel):
  return hex_chunk(pixel[0]) + hex_chunk(pixel[1]) + hex_chunk(pixel[2]) + hex_chunk(pixel[3])


def get_pixels(fpath, ignore_colors = []):
  img = cv2.imread(fpath, cv2.IMREAD_UNCHANGED)
  pixels = {}

  for row in img:
    for pixel in row:
      if pixel[3] != 0:
        hex_pixel = pixel_to_rgba(pixel)
        if hex_pixel not in ignore_colors:
          if hex_pixel in pixels:
            pixels[hex_pixel] += 1
          else:
            pixels[hex_pixel] = 1
  return pixels


print(get_pixels('samples/sprite1.png'))
