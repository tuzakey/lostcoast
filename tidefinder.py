#!/usr/bin/python
'''
A quick^h^h^h^h^h dirty script to find the optimal time to hike the lost coast trail.
'''

import tidetable
import astral
import pytz
from datetime import datetime,timedelta
from dateutil import tz
from pprint import pprint

#Shelter Cove
STATION=9418024

#Calendar year to search
YEAR=2017

#Impassible sections generally are impassible at 3-3.5 ft, we'll play it safe at 2ft
LOWMAX = 2

#we need 2-3 hours on each side of the low tide
SUNRISEPAD = 5
SUNSETPAD = 5

#Date looks like:
'''
[{'datetime': datetime.datetime(2016, 5, 31, 13, 30),
  'high_low': u'L',
  'pred_cm': 21.0,
  'pred_ft': 0.7},...]
'''

def timeokay(dategiven,astralloc):
  fixdate = pytz.UTC.localize(dategiven)
  daylight = astralloc.sun(date=fixdate.date())
  sunrisepaddedtime = daylight['sunrise'] + timedelta(hours=SUNRISEPAD)
  sunsetpaddedtime = daylight['sunset'] - timedelta(hours=SUNSETPAD)
  if (fixdate >= sunrisepaddedtime and fixdate <= sunsetpaddedtime):
    return True
  else:
    return False

if __name__ == "__main__":
  #set up location in Astral to get sunrise/set
  a = astral.Astral()
  a.solar_depression='civil'
  l = astral.Location()
  l.name = "Shelter Cove"
  l.region = 'California'
  l.latitude = 40.0304
  l.longitude = -124.0731
  l.timezone = 'GMT'
  l.elevation = 0

  #we'll need to convert to pacfic later
  fromzone = tz.gettz('UTC')
  tozone = tz.gettz('America/Los_Angeles')

  #fetch in GMT so we don't have to calculate offsets in a bajillion places
  tides = tidetable.get(STATION,year=YEAR,time_zone=tidetable.GMT)
  passable = [x for x in tides if ( x['high_low']=='L' and x['pred_ft'] <= LOWMAX)]

  print("Found {} passable low tide points".format(passable.__len__()))
  doable = [x for x in passable if timeokay(x['datetime'],l)]
  print("Found {} doable low time points".format(doable.__len__()))
  for m in doable:
    d=pytz.UTC.localize(m['datetime']).astimezone(tozone)
    print("Date: {}\nTime: {}\nLow Ft: {}\nMoon: {}\n".format(d.date(),d.time(),m['pred_ft'],l.moon_phase(d.date())))
  print("Moon phases: 0:new, 7:first q, 14:full, 21:last q")


