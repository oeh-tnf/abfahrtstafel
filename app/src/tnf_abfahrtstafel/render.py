from itertools import islice
from datetime import timedelta
from zoneinfo import ZoneInfo
import math
import os
from PIL import Image, ImageDraw, ImageFont

tz = ZoneInfo("Europe/Vienna")

width = 960
height = 680

font = ImageFont.truetype(os.path.join(os.path.dirname(__file__),'Roboto-Bold.ttf'), 100)
smallfont = ImageFont.truetype(os.path.join(os.path.dirname(__file__),'Roboto-Regular.ttf'), 60)
tinyfont = ImageFont.truetype(os.path.join(os.path.dirname(__file__),'Roboto-Regular.ttf'), 12)
semifont = ImageFont.truetype(os.path.join(os.path.dirname(__file__),'Roboto-Bold.ttf'), 75)
extrasmallfont = ImageFont.truetype(os.path.join(os.path.dirname(__file__),'Roboto-Bold.ttf'), 30)

def render_departures(departures, time):
  image = Image.new('1', (width, height), 1)
  draw = ImageDraw.Draw(image)

  yoff = 0
  if 'SE' in departures:
    if departures['SE'][0]['reltime'] / timedelta(minutes=1) < 100:
      render_tram(draw, yoff, 'SE', departures['SE'][:5])
      yoff += 110  
  if '1' in departures:
    if departures['1'][0]['reltime'] / timedelta(minutes=1) < 100:
      render_tram(draw, yoff, '1', departures['1'][:5])
      yoff += 110
  if '2' in departures:
    if departures['2'][0]['reltime'] / timedelta(minutes=1) < 100:
      render_tram(draw, yoff, '2', departures['2'][:5])
      yoff += 110
  if 'N82' in departures:
    if departures['N82'][0]['reltime'] / timedelta(minutes=1) < 100:
      render_tram(draw, yoff, 'N82', departures['N82'][:5])
      yoff += 110

  yoff += 10
  draw.rectangle([0,yoff,width,height], fill=0)

  show_77_in_bus_list = True
  for dep in sorted([ x for xs in departures.values() for x in xs], key=(lambda d: d['abstime'])):
    minutes = math.floor(max(dep['reltime'] / timedelta(minutes=1), 0))
    if show_77_in_bus_list and dep['mode'] == 'bus77' and minutes < 100:
      render_bus_77(draw, yoff, '77', departures['77'][:5])
      show_77_in_bus_list = False
      yoff += 110
    if dep['mode'] == 'bus' and minutes < 100:
      render_bus(draw, yoff, dep)
      yoff += 110
    if yoff > height:
      break

  draw.text((width-2, 0),time.astimezone(tz).strftime("%H:%M"), font=tinyfont, anchor="ra", fill=0);

  return image

def render_tram(draw, yoffset, line, line_deps):
  draw.rounded_rectangle([10,yoffset+10,10+200,yoffset+10+100], 16, fill=0)
  draw.text((10+100, yoffset+5), line, font=font, anchor="ma", fill=1)

  xoffset = 380
  for dep in line_deps:
    minutes = math.floor(max(dep['reltime'] / timedelta(minutes=1), 0))
    if minutes < 100:
      if dep["special"]:
        draw.text((xoffset, yoffset+5), f'{minutes}\'', font=semifont, anchor="ra", fill= 0)
        draw.text((xoffset, yoffset+78), f'{dep["dest"][11:20]+"."}', font=extrasmallfont, anchor="ra", fill=0)
      else:
        draw.text((xoffset, yoffset+5), f'{minutes}\'', font=font, anchor="ra", fill= 0)
      xoffset += 190

def render_bus_77(draw, yoffset, line, line_deps):
  draw.rounded_rectangle([10,yoffset+10,10+200,yoffset+10+100], 16, fill=1)
  draw.text((10+100, yoffset+5), line, font=font, anchor="ma", fill=0)
  draw.text((240,yoffset+25), line_deps[0]['dest'], font=smallfont, fill=1)

  xoffset = 760
  if len(line_deps) == 1:
    xoffset += 190
  for dep in line_deps:
    minutes = math.floor(max(dep['reltime'] / timedelta(minutes=1), 0))
    if minutes < 100:
      if dep["special"]:
        draw.text((xoffset, yoffset+5), f'{minutes}\'', font=semifont, anchor="ra", fill= 0)
        draw.text((xoffset, yoffset+80), f'{dep["dest"][11:23]+"."}', font=extrasmallfont, anchor="ra", fill=1)
      else:
        draw.text((xoffset, yoffset+5), f'{minutes}\'', font=font, anchor="ra", fill= 1)
      xoffset += 190

def render_bus(draw, yoffset, dep):
  draw.rounded_rectangle([10,yoffset+10,10+200,yoffset+10+100], 16, fill=1)
  draw.text((10+100, yoffset+5), dep['line'], font=font, anchor="ma", fill=0)

  draw.text((240,yoffset+25), dep['dest'], font=smallfont, fill=1)
  draw.rectangle([width-150, yoffset+10,width,yoffset+10+100], fill=0)

  minutes = math.floor(max(dep['reltime'] / timedelta(minutes=1), 0))
  draw.text((380+3*190, yoffset+5), f'{minutes}\'', font=font, anchor="ra", fill=1)
