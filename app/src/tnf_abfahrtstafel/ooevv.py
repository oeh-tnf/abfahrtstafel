from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import requests

stops = {
  'jku': '444110100',
}

tz = ZoneInfo("Europe/Vienna")

def get_raw_departures(stop):
  return requests.post('https://verkehrsauskunft.ooevv.at/bin/mgate.exe', json={
    "ver": "1.59",
    "lang": "deu",
    "auth": {
      "type":"AID",
      "aid":"wf7mcf9bv3nv8g5f",
    },
    "client":{
      "type":"WEB",
    },
    "svcReqL": [{
      "req": {
        "stbLoc": {
          'lid': f'L={stop}',
        },
        "jnyFltrL": [{
          "type":"PROD",
          "mode":"INC",
          "value":1088
        }],
        "type":"DEP",
        "sort":"PT",
        "maxJny":40
      },
      "meth":"StationBoard",
    }]
  }).json()

def get_departures(now, stop):
  raw = get_raw_departures(stop)['svcResL'][0]['res']
  deps = {}
  for dep in raw['jnyL']:
    line = raw['common']['prodL'][dep['prodX']]['number']
    destname = dep['dirTxt']

    rawdate = dep['date']
    rawtime = dep['stbStop'].get('dTimeR', dep['stbStop']['dTimeS'])

    year = int(rawdate[-8:-4])
    month = int(rawdate[-4:-2])
    day = int(rawdate[-2:])
    dayoffset = int(rawtime[0:-6]) if len(rawtime) > 6 else 0
    hour = int(rawtime[-6:-4])
    minute = int(rawtime[-4:-2])
    second = int(rawtime[-2:])

    time = datetime(year, month, day, hour, minute, second, tzinfo=tz)
    time += timedelta(days = dayoffset)

    if line not in deps:
      deps[line] = []
    deps[line].append({
      'line': line,
      'mode': 'bus',
      'dest': destname,
      'abstime': time,
      'reltime': time-now,
      'special': False,
    })
  return deps

