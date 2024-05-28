from datetime import datetime, timezone
import requests

stops = {
  'jku_bim': 'at:44:41101',
}

def get_raw_departures(stop):
  return requests.get('https://www.linzag.at/linz-efa/XML_DM_REQUEST',
    params = {
      'mode':'direct',
      'name_dm':stop,
      'outputFormat':'rapidJSON',
      'type_dm':'any',
      'useRealtime':'1',
    }).json()

def get_absolute_departures(stop):
  raw = get_raw_departures(stop)
  deps = {}
  for dep in raw['stopEvents']:
    line = dep['transportation']['number']
    time = dep.get('departureTimeEstimated',dep['departureTimePlanned'])
    if line not in deps:
      deps[line] = []
    deps[line].append(datetime.fromisoformat(time))
  return deps

def get_relative_departures(stop):
  now = datetime.now(timezone.utc)
  absolute = get_absolute_departures(stop)
  rel = {}
  for line in absolute.keys():
    rel[line] = list(map(lambda atime : atime-now ,absolute[line]))
  return rel
