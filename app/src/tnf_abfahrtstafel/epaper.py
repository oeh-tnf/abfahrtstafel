import os

from datetime import datetime, timezone
from PIL import ImageShow
from waveshare_epd import epd13in3k

from . import linzag, render, ooevv

def epaper_main():
  epd = epd13in3k.EPD()
  epd.init();

  print("initialized")

  now = datetime.now(timezone.utc)
  deps = linzag.get_departures(now, linzag.stops['jku']) | ooevv.get_departures(now, ooevv.stops['jku'])
  image = render.render_departures(deps, now)

  print("rendered")

  epd.display(epd.getbuffer(image))

  print("shown")

  os._exit(0)
