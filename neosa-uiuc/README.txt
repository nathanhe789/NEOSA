
<author Joe Tan>

IMPORTANT! PLEASE READ THE FOLLOWING CAREFULLY

  If you are using BOOTSTRAP please save all formatting files in the "bootstrap" folder.
    When referencing any files in the bootstrap folder simply use the following line:

      /bootstrap/file_name.txt
                or
      /bootstrap/folder_name/file_name.txt

Any file that ENDS WITH .html please save it in the templates folder!

I noticed that in the html files you guys are using href="file.html" to call a new page. DON'T DO THIS
  Since we are using Google App Engine to deploy our code, please use the following syntax:

    href="/filename" to reference an html page.

    If you are creating a new html page and needs to reference it, additional codes must be added on the backend
    for the page to render. I will outline the steps below:
      In the "main.py" file you must create a new class.
        It will look something like this:

          class MainHandler(webapp2.RequestHandler):
              def get(self):
                  template = jinja_environment.get_template('templates/index.html')
                  self.response.out.write(template.render())

        You will have to create a new class name with one parameter, something like:

          FilenameHandler(webapp2.RequestHandler):

        Then you must make a function, for the purpose of rendering a page it is very simple to code

              def get(self):
                    template = jinja_environment.get_template('templates/index.html')  <---THIS FUNCTION WILL RENDER THE index.html PAGE
                    self.response.out.write(template.render())

        In order to render your own page simply change the "index.html" to "your_file_name.html"

        After doing all of that you have to add one more line to the very end of the python file
        You will see something like this:

          app = webapp2.WSGIApplication([
              ('/map', MapHandler),
              ('/calendar', CalendarHandler),
              ('/about', AboutHandler),
              ('/signup', SignUpHandler),
              ('/login', LoginHandler),
              ('/.*', MainHandler)
          ], debug=True)

      Simply add ('/filename', FilenameHandler), to the code right before ('/.*', MainHandler)
