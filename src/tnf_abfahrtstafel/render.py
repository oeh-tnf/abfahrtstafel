import os
from datetime import timedelta
import math
from PIL import Image, ImageDraw, ImageFont

width = 960
height = 680

font = ImageFont.truetype(os.path.join(os.path.dirname(__file__),'Roboto-Bold.ttf'), 100)

def render_departures(departures):
  image = Image.new('1', (width, height), 255)
  draw = ImageDraw.Draw(image)

  draw.rounded_rectangle([10,10,10+65,10+100], 5, fill=0)
  draw.text((15, 5), '1', font=font, fill=1)

  if '1' in departures:
    offset = 200
    for dep in departures['1']:
      minutes = math.floor(max(dep / timedelta(minutes=1), 0))
      if minutes < 100:
        draw.text((offset, 5), f'{minutes}\'', font=font)
        offset += 200

  draw.rounded_rectangle([10,110+10,10+65,110+10+100], 5, fill=0)
  draw.text((15, 110+5), '2', font=font, fill=1)

  if '2' in departures:
    offset = 200
    for dep in departures['2']:
      minutes = math.floor(max(dep / timedelta(minutes=1), 0))
      if minutes < 100:
        draw.text((offset, 110+5), f'{minutes}\'', font=font)
        offset += 200

  return image
