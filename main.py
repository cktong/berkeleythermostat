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

class Users(db.Model): # to log users
     user_id=db.IntegerProperty(required = True)
     user_name=db.StringProperty(required = True)
     user_password=db.StringProperty(required = True)
     user_ip=db.StringProperty(required = True)
     user_zip=db.IntegerProperty(required = True)         
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
    
    def post(self):
        user_name = self.request.get('user_name')

        self.redirect('/results?username=' + user_name)  
        
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
      
      userinfo = db.GqlQuery("select * from Users")
      
      for u in userinfo:
            indoor_temperature=float(get_indoor_temperature(u.user_ip)) 
            outdoor_temperature=float(get_outdoor_temperature(u.user_zip))
            mode=int(tmodeget(ip))
            
            #self.response.write('Indoor temperature: %s' % str(indoor_temperature))
            #self.response.write('Outdoor temperature: %s' % str(outdoor_temperature))
            #self.response.write('Mode: %s' % str(mode))
        
            if indoor_temperature and outdoor_temperature:
               p = Post(parent = blog_key(), user_id=user_id, indoor_temperature = indoor_temperature, outdoor_temperature = outdoor_temperature, mode=mode)
               p.put()
         
               print p.indoor_temperature
               print p.mode
               self.response.write('Success!')
            else:
               self.response.write('Error apending to db')
           
class Results(WebHandler): #handler for /blog
    def get(self):
      posts = db.GqlQuery("select * from Post order by datetime desc")
      
      #print posts.__class__.__name__
     
      self.render('results.html',posts=posts)     
      
#--------------------------------signup-------------------------------------------------------------#

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

ZIPCODE_RE = re.compile(r"^[0-9]{5}$")
def valid_zipcode(zipcode):
    return zipcode and ZIPCODE_RE.match(zipcode)
    
#def unique_entry(username, zipcode, ip):
#    userinfo = Users.gql("WHERE user_name=%s and user_zip= %s and user_ip=%s" %(username, zipcode, ip))
#    userinfo = Users.gql("WHERE user_id=%s and user_zip= %s" %(userid, zipcode))
#    return user_id
    
class Signup(WebHandler):

    def get(self):
        #users.create_login_url(dest_url='/results')
        self.render("signup-form.html")
        
    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        zipcode= self.request.get('zipcode')
        ip=self.request.get('ip')
         
        params = dict(username = username,
                      email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True
            
        if not valid_zipcode(zipcode):
            params['error_zipcode'] = "That's not a valid zipcode."
            have_error = True
        
        #if not unique_entry(username, zipcode, ip):
         #   params['error_repeatuser'] = "This user has been registered before"
         #   have_error = True
        
        if have_error:
            self.render('signup-form.html', **params)
        else:   
            
            u = Users(parent = blog_key(), user_id=1, user_name=username, user_password = password, user_ip=ip, user_zip=int(zip))
            u.put()
            #u=Users(parent=blog_key(), 
            
            self.redirect('/results?username=' + username)     
    
#---------------------------------------------------------------------------------------------------# 
      
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', Signup),    
    ('/login', Login),
    ('/results', Results),
    ('/gettemperature', GetTemperature)
], debug=True)