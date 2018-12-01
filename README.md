# Homework 7: Websites and APIs

Due: Sunday, December 2, 8pm
What to turn in:
* app.yaml: your YAML file
* any Python files your app uses (there should be at least one!)
* any HTML templates your app uses (there should be at least one, probably two)
* any CSS, JavaScript, or image files your app uses (optional)
* a URL to your program on app engine (via Canvas)

Note: for Github Classroom turn ins, please remember to check your repository website to make sure you have both committed the most recent version of your code and pushed it to the server!

## Part 1 (and only): Your Web App. 
For this assignment, you must create a web application that accepts user input, uses that input to query an API, and then outputs the results. Your application must run on Google App Engine. You may either:

1. Use an API you are considering for your project (but not the DarkSky or Spotify APIs)
2. Use the Flickr API

If you are a bit shakier in App Engine or APIs, we recommend doing this homework with Flickr as we have more in-class demos and example code using the Flickr API. Similarly, if your API requires oAuth, we *strongly* recommend that you do this homework with Flickr before making your work more complicated for the project.

We provide instructions for the Flickr API below. Adapt as necessary if you are using a different API. 

### Flickr instructions

Your goal in this assignment is to create a web app that lets you search Flickr and that displays thumbnails from the results. The minimum requirements, if using the Flickr API, are that:

1. **Your app have a webpage that takes a user's input for one or more things for which to search (this could be text, it could be a tag, it could be a location, etc.).**

2. **Your app search Flickr based in this user input and display at least five thumbnails.**

    Note: Pages on App Engine have a maximum execution time. As you experienced in HW6, conducting a search for 500 images, or even calling `flickr.photos.getinfo` on several photos, can take a long time. We recommend keeping your `per_page` count low, and, at least at first, using just `flickr.photos.search` to generate your results. 

3. **Your app should run on Google App Engine.**

    That's it, though you are welcome to add more, especially to practice HTML and CSS.
 
#### Suggestions and Guidance

There are several ways you can go about this – figuring out how to put together what you have learned about APIs, App Engine, and Python is the primary goal of this assignment. 

If you are unsure where to start, we suggest following these steps:

1. Take a look at the postapp from class again and get comfortable with it. Make sure you can run it locally using `dev_appserver.py` (remember to include the path for your homework!) and that you can upload it to Google App Engine using `gcloud app deploy`.
 
2. Ignore user input at first, and work on having App Engine talk to Flickr. Once you are able to talk to the Flickr API and output images as HTML, it will be a lot easier to test user input. To work on the output:

    a.	Copy your flickrREST code from HW6 into the given `main.py`.

    b.	Edit FlickrSearchResponseHandler, and call flickREST. Note: to view the output you are getting, you can either log it or insert it into vals and modify the template to print it. Please reference the GreetHandler in the `main.py` of the postapp example.  

    c.	Once you have your code accessing the Flickr API, it’s time to focus on the output a bit. Modify the vals dictionary and the template (greetresponse.html, or create a new one and update main.py) to loop through the photo results. 
	
    **Hint 1:** Recall that you can write loops in your Jinja template using `{% for item in somevariable %}`, `{{item}}`, and `{% endfor %}`

    **Hint 2:** Read the Flickr API documentation to figure out how to reference photos of different sizes.

    **Hint 3:** As you work on these steps, you should be able to test by just visiting the web page (either locally or on App Engine) and hitting submit. 

3.	Now, let's work on user input. The simplest thing to do is to search for a tag or text, using the input field that already exists for “name”. The next few steps will assume that you are doing that, but you are welcome to take a different approach. 

    a.	First, let's update `flickrsearchform.html`. You can reference the `greetform.html` from the postapp example.  If you use greetform.html, just open it and edit the text to provide a prompt for the user. You can also change the name and id attributes for the username field, if you like. Since we aren’t using greet_type, delete that. We have a `flickrsearchform.html` file for you to start from.

    b.	Now we can update our main.py again. We really only need to do one thing: make sure that the user input gets passed to `flickrREST`. If you didn’t edit the name attribute in flickrsearchform.html, you can just pass `self.request.get('username')` right into `flickrREST` as either a tag or text (see your HW6 for how you did that). If you did edit the name attribute -- and you eventually should so that your variable name is meaningful -- you just have to make sure the variable names match. 

    c.	Go ahead and test it. Hopefully everything is working. 

4.	As some cleanup, go into `main.py` and delete any functions that are no longer used.  

## Python 2.7, Google App Engine, and urllib
In Python2.7 and Google App Engine, we don't have access to the same `urllib` as in Python 3. You will need to use:

* `urllib.urlencode` instead of `urllib.parse.urlencode`. It otherwise works the same way. You can access this function if you `import urllib`.

* Instead of `urllib.request`, you will need to use `urlfetch` from Google's APIs. See the [documentation](https://cloud.google.com/appengine/docs/standard/python/issue-requests). Note: if your API requires that you send data as part of headers, you may need to use the `requests` module, also documented on that page.

Finally, you may have to deal with unicode characters (the same thing Ostin, John, and Alex were struggling with in class on Tuesday). Python 2.7 doesn't deal with this as well as 3 (and 3 isn't always a walk in the park either), but for most Flickr searches you can deal with it by replacing Unicode characters that aren't in ASCII with nothing or a placeholder:
```python
mystr = mystr.encode('ascii','replace')
```
[More details on the Python website](https://docs.python.org/2/howto/unicode.html).