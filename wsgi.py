# This file contains the WSGI configuration required to serve up your
# web application.
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Bottle project
import bottle
import os
import sys
here = os.path.dirname(__file__)
# add your project directory to the sys.path
project_home = os.path.join(here, "src/")
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# make sure the default templates directory is known to Bottle
templates_dir = os.path.join(project_home, 'server/views/')
if templates_dir not in bottle.TEMPLATE_PATH:
    bottle.TEMPLATE_PATH.insert(0, templates_dir)

from server.control import application

if __name__ == "__main__":
    bottle.run(host='localhost', port=8080)
