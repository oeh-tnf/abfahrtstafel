from datetime import datetime, timezone
import re
import requests

stops = {
  'jku': 'at:44:41101',
}

lines = {
  '1': {
    'default_dest':'60501810', # Auwiesen
    'mode':'tram'
  },
  '2': {
    'default_dest':'60500296', # Solar City
    'mode':'tram'
  },
  'N82': {
    'default_dest':'60500296', # Solar City
    'mode':'tram'
  },
  '77': {
    'default_dest':'60501720', # Hauptbahnhof
    'mode':'bus'
  }
}

ignore_dests = [
  '60500921', # JKU Nord
]

def get_raw_departures(now, stop):
  return requests.get('https://www.linzag.at/linz-efa/XML_DM_REQUEST',
    params = {
      'mode':'direct',
      'name_dm':stop,
      'outputFormat':'rapidJSON',
      'type_dm':'any',
      'useRealtime':'1',
      'itdDate': now.strftime("%Y%m%d"),
      'itdTime': now.strftime("%H%M"),
    }).json()

def get_departures(now, stop):
  raw = get_raw_departures(now, stop)
  deps = {}
  for dep in raw['stopEvents']:
    line = dep['transportation']['number']
    destid = dep['transportation']['destination']['id']
    time = datetime.fromisoformat(dep.get('departureTimeEstimated',dep['departureTimePlanned']))
    if destid in ignore_dests:
      continue
    if line not in deps:
      deps[line] = []
    deps[line].append({
      'line': line,
      'mode': lines[line]['mode'],
      'dest': dep['transportation']['destination']['name'],
      'abstime': time,
      'reltime': time-now,
      'special': destid != lines[line]['default_dest']
    })
  return deps
