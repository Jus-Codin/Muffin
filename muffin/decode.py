from PIL import Image
from textwrap import wrap

def get_coords(n, width):
  """Get the coordinates of nth pixel"""
  y, x = divmod(n, width)
  return x-1, y

def pack(arr, key):
  val = 0
  for i in arr[::-1]:
    val = val * key + i
  return val - key

class MuffinDecoder:
  DEFAULT_KEY = (89, 66, 78) # Ord of YBN

  def __init__(self, key: tuple=DEFAULT_KEY):
    self.key = key

  def set_key(self, key: tuple):
    self.key = key

  def get_headers(self, header_len: int, img: Image.Image):
    width = img.size[0]
    
    length_header = []
    step_header = []
    for i in range(header_len):
      length, step, _ = img.getpixel(get_coords(i+1, width))
      length_header.append(length)
      step_header.append(step)

    return pack(length_header, self.key[0]), pack(step_header, self.key[1])

  def decode(self, image_name) -> str:
    img = Image.open(image_name)
    return self._decode(img)

  def _decode(self, image: Image.Image):
    width, height = image.size
    header_len = image.getpixel((0, 0))[2] - self.key[2]

    length, step = self.get_headers(header_len, image)

    data_len = (length // 3 + 1) * step 
    start = header_len + 1

    data = ""
    for i in range(start, start+data_len, step):
      bits = image.getpixel(get_coords(i, width))
      data += "".join(str(i & 1) for i in bits)

    msg = ""
    for char in wrap(data, 8):
      if len(char) == 8:
        msg += chr(int(char, 2))

    return msg
