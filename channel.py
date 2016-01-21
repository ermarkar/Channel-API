

# Author :Sunil Garg
import os
from google.appengine.api import channel
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
from google.appengine.ext import db

#datastore class to save channel token coreesoinding to registered user
class User(db.Model):
  email = db.StringProperty()
  channelToken = db.StringProperty()

class SendMessage(webapp.RequestHandler):
    def post(self):
        messageToId = self.request.POST.get("messageToId")
        message = self.request.POST.get("message")
        
        if message == '': # message field of send_message can't be empty
            message = " "
        user_k = db.Key.from_path('User', messageToId) # get keys based on key_name 
        user = db.get(user_k) # get object of User class based on searched key_name
        
        channel.send_message(user.channelToken,message)
        

class CreateChannel(webapp.RequestHandler):
    def post(self):
        userEmail = self.request.POST.get("userId")
        logging.info('USer Email in create channel :'+ str(userEmail))
        channelToken = channel.create_channel(userEmail)
        logging.info('Channel Token : ' + channelToken)
        user = User(key_name=userEmail,email=userEmail,channelToken=channelToken) #create tuple for USer entity in datastore
        user.put()
        self.response.out.write(channelToken)

class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'index.html')

        self.response.out.write(template.render(path, template_values))
    
application = webapp.WSGIApplication([
    ('/', MainPage),('/createchannel',CreateChannel),('/sendmessage',SendMessage)], debug=True)


def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
