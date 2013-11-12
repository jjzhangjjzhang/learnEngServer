import cgi
import json
import urllib

from google.appengine.ext import ndb
import webapp2


MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/query" method="post">
      <div><textarea name="essayId" rows="3" cols="60"></textarea></div>
      <div><textarea name="level" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="query essay"></div>
    </form>
    
    <form action="/insert" method="post">
      <div><textarea name="essayId" rows="3" cols="60"></textarea></div>
      <div><textarea name="level" rows="3" cols="60"></textarea></div>
      <div><textarea name="essayContent" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="essay info"></div>
    </form>
    
  </body>
</html>
"""

class Level(ndb.Model):
    level = ndb.IntegerProperty()

class Essay(ndb.Model):
    essayId = ndb.IntegerProperty()
    content = ndb.StringProperty()
    
    @classmethod
    def queryEssay(cls, essayId1, level):
        return cls.query( cls.essayId=essayId1, parent=ndb.Key("Level", level) ) 


# Query from HTTP POST message
class QueryEssay(webapp2.RequestHandler):
    def post(self):
        essayId = int( self.request.get('essayId') ) 
        level = int( self.request.get('level') )  
        levelKey = ndb.Key("Level", level)
        essay = Essay.queryEssay( essayId, level )
        #essay = qry.filter(Essay.essayId=essayId)
        self.response.headers['Content-Type'] = 'application/json'  
        self.response.out.write( json.dumps(essay) )
     
# Store request from HTTP POST message
class InsertEssay(webapp2.RequestHandler):  
    def post(self):
   
        level = int( self.request.get('level') )
        levelEntity = Level()
        levelEntity.level = level
        levelEntity.put() 
        
        content = self.request.get('essayContent')
        essayEntity = Essay( parent=ndb.Key("Level", level) )
        
        essayEntity.essayId = int( self.request.get('essayId') )
        essayEntity.content = content
        essayEntity.put()
    
class DeleteEssay(webapp2.RequestHandler):  
    def post(self):
        essayId = int( self.request.get('essayId') )
        level = int( self.request.get('level') )
        essay = Essay.query(ancestor=ndb.Key("Level", level), essayId=essayId).fetch(1) 
        essay.key.delete()
    
class ModifyEssay(webapp2.RequestHandler):  
    def post(self):
        essayId = int( self.request.get('essayId') )
        level = int( self.request.get('level') )
        essay = Essay.query( ndb.AND(ancestor=ndb.Key("Level", level), essayId=essayId) ).fetch(1) 
        content = self.request.get('essayContent')
        essay.content = content
        essay.put()
        
class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write(MAIN_PAGE_HTML)
# Structure of server website 
application = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/query', QueryEssay),
  ('/insert', InsertEssay),
  ('/delete', DeleteEssay),
  ('/modify', ModifyEssay),
], debug=True)