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

# Initial generic HTML 'header' output

print "Content-type: text/html\n\n";
print "<html><head><title>Effrecipes -- List of all Recipes</title>\n"
print "<h1>List of All Recipes</h1></head>\n\n"


# Show complete list of records

print "<b>Select a record to view:</b>\n"

print "<table border=1>\n"

recipelist = effrecipes.recipe_list(None, conn)
for record in recipelist:
  print "<tr>"
  print '<td><a href="RecipeDisplay.cgi?Id=' + str(record.RecipeId) \
        +'">', record.Name, '</a></td>'
  print "</tr>\n"

print "</table><br/>"

print '<a href="../write/RecipeEdit.cgi?Id=new">Enter new recipe.</a><br/>'

print '<a href="../../index.html">Back to front page.</a><br/>'

# Cleanup and exit
print "</html>"
conn.close()
