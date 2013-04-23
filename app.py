import urllib2 as net #defines functions and classes which help in opening URLs (mostly HTTP)

import json # is a lightweight data interchange format based on a subset of JavaScript syntax

from xml.dom.minidom import parseString
            
def get_indoor_temperature(IP):
   url= "http://" + IP + "/tstat/temp" #creates string with IP address of location of thermostat 
   file = net.urlopen(url) # file is a file like object that is returned when opening the url
   #print file.__class__.__name__
   file.close
   tempread= file.read() #tempread is a str that is extracted read from 'file' 
   #print tempread.__class__.__name__
   jsonData=json.loads(tempread) #json.loads takes a string object formated as json and turns it into a json object
   temperature=jsonData['temp'] #as a json object, information can be easily retrieved by calling on member 'temp'
   
   return temperature

def get_outdoor_temperature(zip):
   url= "http://api.wxbug.net/getLiveCompactWeatherRSS.aspx?ACode=A3452221584&zipcode=" + zip
   file = net.urlopen(url)   # file returned as a file like object
   data = file.read() # data is a str that has a XML type format
   #print data.__class__.__name__
   file.close()
   dom = parseString(data)    #parse the XML like string into a document object
   
   xmlTag = dom.getElementsByTagName('aws:temp') #retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName
   #print xmlTag
   temperature=xmlTag.item(0).firstChild.nodeValue    #xmlTag is now a node list, grab nodeValue from the first item
   return temperature

def tmodeget(IP):
   # same documentation as get_indoor_temperature furnction
   url= "http://" + IP + "/tstat/tmode"
   opentMode= net.urlopen(url)
   tMode=opentMode.read()
   jsontMode=json.loads(tMode)
   getmode=jsontMode['tmode']
   return getmode
   
def tmodeset(IP,postmode): 
   url= "http://" + IP + "/tstat/tmode"
   tmodestring= '{"tmode":' + str(postmode) + '}' #create a string that can be used to POST mode to thermostat
   net.urlopen(url,tmodestring)  # mode string is a data parmeter which will cause urlopen to be a POST method
   print "Mode set to " + str(postmode)
   

   

   
