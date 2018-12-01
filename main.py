#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, urllib, urllib2, webbrowser, json
import jinja2

import os
import logging

FLICKR_KEY = 'b5649f05223a5e2eaae47bad728c7982'

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

 
def safeGet(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        print ('The server couln\'t fulfill the request.')
        print ('Error code: ', e.code)
    except urllib2.URLError as e:
        print ('We failed to reach a server')
        print ('Reason: ', e.reason)
    return None

def flickrREST(baseurl = 'https://api.flickr.com/services/rest/',
               method = 'flickr.photos.search',
               api_key = FLICKR_KEY,
               format = 'json',
               params={},
               ):
    params['method'] = method
    params['api_key'] = api_key
    params['format'] = format
    if format == "json": params["nojsoncallback"]=True
    url = baseurl + "?" + urllib.urlencode(params)
    return safeGet(url)
   
def get_photo_ids(tag="Seattle", latlng = None, n=20):
    params = {'tags': tag, 'per_page':n}
    if latlng != None:
        #handle lat lng search
        lat, lng = latlng.split(",")
        params["lat"] = lat
        params["lon"] = lng
        params['radius'] = "20"
        params['radius_units'] = "km"
    
    data_retrieved = flickrREST(params = params)
    if (data_retrieved != None):
        data_read = data_retrieved.read()
        data_load = json.loads(data_read)
        photo_list = data_load['photos']['photo']
        id_list = []
        for each in photo_list:
            id_list.append(each['id'])
        return id_list
    else:
        return None
   
def get_photo_info(photo_id):
    data_retrieved = flickrREST(method = "flickr.photos.getInfo", params=({'photo_id':photo_id}))
    if (data_retrieved != None):
        data_read = data_retrieved.read()
        data_load = json.loads(data_read)
        return data_load['photo']
    else:
        return None

def get_photo_sizes(photo_id):
    data_retrieved = flickrREST(method = "flickr.photos.getSizes", params=({'photo_id':photo_id}))
    if (data_retrieved != None):      
        jsonresult = data_retrieved.read()
        d = json.loads(jsonresult)
        d = d['sizes']['size'][2]['source']
    return d
    
class Photo():
    def __init__(self, photosdict):
        self.title = photosdict['title']['_content'].encode('utf-8')
        self.author = photosdict['owner']['username'].encode('utf-8')
        self.userid = photosdict['owner']['nsid']
        self.tags = [tag['_content'] for tag in photosdict['tags']['tag']]
        self.num_views = int(photosdict['views'])
        self.commentcount = int(photosdict['comments']['_content'])
        self.url = photosdict['urls']['url'][0]['_content']
        self.photo_url = get_photo_sizes(photosdict['id'])
    
    def __str__(self):
        s = "Title: %s / Author: %s" %(self.title, self.author)
    
    def open_url(self):
        webbrowser.open(self.url)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("In MainHandler")
             
        template_values={}
        template_values['page_title']="Flickr Search"
        template = JINJA_ENVIRONMENT.get_template('flickrsearchform.html')
        self.response.write(template.render(template_values))        
        
class FlickrSearchResponseHandler(webapp2.RequestHandler):
    def post(self):
        latlng = self.request.headers.get("X-AppEngine-CityLatLong",None)
        vals={}
        search_input = self.request.get('search_input')
        vals['page_title']="Flickr Search Results: " + search_input
                  
        if search_input:

            vals['search_input']=search_input
            photos = [Photo(get_photo_info(photo_id)) for photo_id in get_photo_ids(search_input,latlng)]
                    
            #Top Five Photos by Views
            topviews = sorted(photos, key=lambda x: x.num_views, reverse=True)
            topfiveviews = []
            for photo in topviews[:5]:
                topfiveviews.append(photo)
            vals['topfiveviews'] = topfiveviews
                    
            #The photo with the highest number of tags
            toptags = sorted(photos, key=lambda x: len(x.tags), reverse=True)
            toponetags = toptags[0]
            vals['toponetags'] = toponetags
                    
            #The photo with the highest number of comments
            topcomments = sorted(photos, key=lambda x: x.commentcount, reverse=True)
            toponecomments = topcomments[0]
            vals['toponecomments'] = toponecomments
            template = JINJA_ENVIRONMENT.get_template('flickrsearchresponse.html')
            self.response.write(template.render(vals))                  
        else:
            template = JINJA_ENVIRONMENT.get_template('flickrsearchform.html')
            self.response.write(template.render(vals))
 
application = webapp2.WSGIApplication([ \
                                      ('/flickersearchresponse', FlickrSearchResponseHandler),
                                      ('/.*', MainHandler)
                                      ], 
                                      debug=True)
