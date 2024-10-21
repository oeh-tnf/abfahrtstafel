from datetime import datetime, timezone
from PIL import ImageShow

from . import linzag, render, ooevv

def show_main():
  now = datetime.now(timezone.utc)
  
  # for testing one can select a specific time for the request here:
  #datetime_str = '21/10/24 7:50:00'
  #now = datetime.strptime(datetime_str, '%d/%m/%y %H:%M:%S')

  print('Hello, World!')
  deps = linzag.get_departures(now, linzag.stops['jku']) | ooevv.get_departures(now, ooevv.stops['jku'])
  print(deps)
  ImageShow.show(render.render_departures(deps, now))
