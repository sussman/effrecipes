#!/usr/bin/env python2


import cgi

# enable debugging:  displays detailed exceptions in web browser.
import cgitb; cgitb.enable()

import MySQLdb

# temporary:  eventually put 'effrecipes.py' into a standard PYTHONPATH
# location, like /usr/lib/python2.3/site-packages/
import sys
sys.path.append('/home/sussman/projects/effrecipes/objects')
import effrecipes


# -----------------------------------------------------------------

# Initialize database connection

conn = MySQLdb.connect(user='effuser', passwd='effuser', db='effrecipes')

# Grab the object from the database

form = cgi.FieldStorage()
val = form["Id"].value   # this better be a valid ID
ingredient = effrecipes.ingredient_lookup(int(val), conn)

# Initial generic HTML 'header' output

print "Content-type: text/html\n\n";
print "<html><head><title>Effrecipes -- Ingredient Display</title>\n"
print '<h1>Ingredient: "' + ingredient.Name + '"</h1></head>\n\n'

print '(click the record to modify it)<br/>'
print "<table border=1><tr><td>IngID</td><td>Name</td></tr>\n"
print "<tr>"
print '<td>', ingredient.IngId, '</td>'
print '<td><a href="../write/IngredientEdit.cgi?Id=' + str(ingredient.IngId) \
        +'">', ingredient.Name, '</a></td>'
print "</tr>\n"

print "</table><br/>"


# Cleanup and exit
print "</html>"
conn.close()
