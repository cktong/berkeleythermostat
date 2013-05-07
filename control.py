# turn thermostat on or off
from random import choice

def control():
   modeoptions= [-1, 0, 1]
   mode = choice(modeoptions)
   return mode
