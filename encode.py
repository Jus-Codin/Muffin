from PIL import Image

import numpy as np

def greedy_zip(*lists, length: int, default=0):
  """Horrible function to greedily zip multiple lists until a set length"""
  a = []
  for i in range(length):
    a.append([it[i] if len(it) > i else default for it in lists])
  return a

def unpack(n, key):
  n += key
  l = [n if n <= 255 else n % key]
  while n > 255:
    n = n // key
    l.append(n if n <= 255 else n % key)
  return l

def get_coords(n, width):
  """Get the coordinates of nth pixel"""
  y, x = divmod(n, width)
  return x-1, y

def set_lsb(n, b):
  return (n & ~1) | b

class MuffinEncoder:
  DEFAULT_KEY = (89, 66, 78) # Ord of YBN

  def __init__(self, key: tuple=DEFAULT_KEY):
    self.key = key

  def set_key(self, key: tuple):
    self.key = key

  def get_header(self, length, step):
    length_header = unpack(length, self.key[0])
    step_header = unpack(step, self.key[1])

    header_len = max(len(length_header), len(step_header))

    return np.array(greedy_zip(length_header, step_header, [header_len+self.key[2]], length=header_len))

  def encode(
     self,
     image_name: str,
     msg: str,
     step: int=1,
     save_name="muffin.png"
  ):
    img = Image.open(image_name)
    img = self._encode(img, msg, step)
    img.save(save_name)

  def _encode(
    self,
    image: Image.Image,
    msg: str,
    step: int=1
  ):
    msg = "".join(format(ord(s), "08b") for s in msg)
    
    data = np.fromiter(map(int, msg), dtype=int)
    data.resize((len(msg)//3+1,3))

    data_len = len(data) * step

    header = self.get_header(len(msg), step)

    if len(image.mode) != 3:
      raise ValueError("Image must have 3 channels!")

    width, height = image.size

    enc = image.copy()

    for i, pixel in enumerate(header):
      xy = get_coords(i+1, width)
      enc.putpixel(xy, tuple(pixel))

    start = len(header) + 1
    for i, bits in zip(range(start, start+data_len, step), data):
      xy = get_coords(i, width)
      rgb = enc.getpixel(xy)
      rgb = [set_lsb(n, b) for n, b in zip(rgb, bits)]
      enc.putpixel(xy, tuple(rgb))

    return enc