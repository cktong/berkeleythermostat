import webapp2
import jinja2
from app import *

import os
import re
from string import letters

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates') #template_dir states that the templates will be in the template folder
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

#--------------------------------database----------------------------------------------------#                                    
                               
def blog_key(name = 'default'): #the data needs to have a parent in google datasore
    return db.Key.from_path('blogs', name)
        
class Post(db.Model): # the db parameters
    datetime = db.DateTimeProperty(auto_now_add = True)
    user_id = db.IntegerProperty(required = True)
    indoor_temperature = db.FloatProperty(required = True)
    outdoor_temperature = db.FloatProperty(required = True)
    mode = db.IntegerProperty(required = True)
    
    def render(self):
        #self._render_text = self.content.replace('\n', '<br>')
        return render_str("results.html", p = self) #p=self is the **param       

#---------------------------------------------------------------------------------------------------#             
                               
def render_str(template, **params): # ** is because we dont know what parameter values would be needed in the template
    t = jinja_env.get_template(template) # get the templates
    return t.render(params) # renders the parameters into the template

class WebHandler(webapp2.RequestHandler):
    def write(self, *a, **kw): # * is if you have an unamed argument eg: write(2) whereas **kw is when you have a named argument write(e=2)
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params): #the params are subsituted into the parameter
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Login(WebHandler):
    def get(self):
        self.render("login.html")    
        
#---------------------------------------------------------------------------------------------------#         

ip="50.131.237.15:8459"
zip="94704"
user_id=1 # each user will have another id

class MainHandler(webapp2.RequestHandler):
   def get(self):

      indoor_temperature=float(get_indoor_temperature(ip)) 
      outdoor_temperature=float(get_outdoor_temperature(zip))
      mode=int(tmodeget(ip))
      #self.response.write('Indoor temperature: %s' % str(indoor_temperature))
      #self.response.write('Outdoor temperature: %s' % str(outdoor_temperature))
      #self.response.write('Mode: %s' % str(mode))
        
      if indoor_temperature and outdoor_temperature:
         p = Post(parent = blog_key(), user_id=user_id, indoor_temperature = indoor_temperature, outdoor_temperature = outdoor_temperature, mode=mode)
         p.put()
         
         print p.indoor_temperature
         #print p.mode
         self.response.write('Success!')
      else:
         self.response.write('Error apending to db')
         

class GetTemperature(webapp2.RequestHandler):
   def get(self):

      indoor_temperature=float(get_indoor_temperature(ip)) 
      outdoor_temperature=float(get_outdoor_temperature(zip))
      mode=int(tmodeget(ip))
      #self.response.write('Indoor temperature: %s' % str(indoor_temperature))
      #self.response.write('Outdoor temperature: %s' % str(outdoor_temperature))
      #self.response.write('Mode: %s' % str(mode))
        
      if indoor_temperature and outdoor_temperature:
         p = Post(parent = blog_key(), user_id=user_id, indoor_temperature = indoor_temperature, outdoor_temperature = outdoor_temperature, mode=mode)
         p.put()
         
         print p.indoor_temperature
         #print p.mode
         self.response.write('Success!')
      else:
         self.response.write('Error apending to db')
           
class Results(WebHandler): #handler for /blog
    def get(self):
      posts = db.GqlQuery("select * from Post order by datetime desc")
      #print posts.__class__.__name__
     
      self.render('results.html',posts=posts)
           
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', Login),
    ('/results', Results),
    ('/gettemperature', GetTemperature)
], debug=True)
