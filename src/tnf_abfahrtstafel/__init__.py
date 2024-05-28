from PIL import ImageShow

from . import linzag, render

def show_main():
  print('Hello, World!')
  deps = linzag.get_relative_departures(linzag.stops['jku_bim'])
  ImageShow.show(render.render_departures(deps))

def epaper_main():
  print('Hello, World!')
