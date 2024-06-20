from datetime import datetime, timezone
from PIL import ImageShow

from . import linzag, render, ooevv

def show_main():
  now = datetime.now(timezone.utc)
  print('Hello, World!')
  deps = linzag.get_departures(now, linzag.stops['jku']) | ooevv.get_departures(now, ooevv.stops['jku'])
  print(deps)
  ImageShow.show(render.render_departures(deps))
