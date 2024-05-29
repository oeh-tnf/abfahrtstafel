from itertools import islice
from datetime import timedelta
import math
import os
from PIL import Image, ImageDraw, ImageFont

width = 960
height = 680

font = ImageFont.truetype(os.path.join(os.path.dirname(__file__),'Roboto-Bold.ttf'), 100)
smallfont = ImageFont.truetype(os.path.join(os.path.dirname(__file__),'Roboto-Regular.ttf'), 60)

def render_departures(departures):
  image = Image.new('1', (width, height), 1)
  draw = ImageDraw.Draw(image)

  yoff = 0
  if '1' in departures:
    render_tram(draw, yoff, '1', departures['1'][:5])
    yoff += 110
  if '2' in departures:
    render_tram(draw, yoff, '2', departures['2'][:5])
    yoff += 110
  if 'N82' in departures:
    render_tram(draw, yoff, 'N82', departures['N82'][:5])
    yoff += 110

  yoff += 10
  draw.rectangle([0,yoff,width,height], fill=0)

  for dep in sorted([ x for xs in departures.values() for x in xs], key=(lambda d: d['abstime'])):
    minutes = math.floor(max(dep['reltime'] / timedelta(minutes=1), 0))
    if dep['mode'] == 'bus' and minutes < 100:
      render_bus(draw, yoff, dep)
      yoff += 110
    if yoff > height:
      break

  return image

def render_tram(draw, yoffset, line, line_deps):
  draw.rounded_rectangle([10,yoffset+10,10+200,yoffset+10+100], 16, fill=0)
  draw.text((10+100, yoffset+5), line, font=font, anchor="ma", fill=1)

  xoffset = 380
  for dep in line_deps:
    minutes = math.floor(max(dep['reltime'] / timedelta(minutes=1), 0))
    if minutes < 100:
      draw.text((xoffset, yoffset+5), f'{"·" if dep["special"] else ""}{minutes}\'', font=font, anchor="ra")
      xoffset += 190

def render_bus(draw, yoffset, dep):
  draw.rounded_rectangle([10,yoffset+10,10+200,yoffset+10+100], 16, fill=1)
  draw.text((10+100, yoffset+5), dep['line'], font=font, anchor="ma", fill=0)

  draw.text((240,yoffset+25), dep['dest'], font=smallfont, fill=1)
  draw.rectangle([width-150, yoffset+10,width,yoffset+10+100], fill=0)

  minutes = math.floor(max(dep['reltime'] / timedelta(minutes=1), 0))
  draw.text((380+3*190, yoffset+5), f'{minutes}\'', font=font, anchor="ra", fill=1)
