from datetime import datetime, timezone
from PIL import ImageShow
import pytz

from . import linzag, render, ooevv

def show_main():
  now = datetime.now(pytz.timezone('Europe/Vienna'))
  
  # for testing one can select a specific time for the request here:
  #datetime_str = '21/10/24 0:50:00 +02:00'
  #now = datetime.strptime(datetime_str, '%d/%m/%y %H:%M:%S %z')

  print('Hello, World!')
  deps = linzag.get_departures(now, linzag.stops['jku']) | ooevv.get_departures(now, ooevv.stops['jku'])
  print(deps)
  ImageShow.show(render.render_departures(deps, now))
