#!/usr/bin/env python2

# Generate an HTML front-page for the Effrecipe Database 

import cgi

# enable debugging:  displays detailed exceptions in web browser.
import cgitb; cgitb.enable()

import MySQLdb

# temporary:  eventually put 'effrecipes.py' into a standard PYTHONPATH
# location, like /usr/lib/python2.3/site-pacakages/
import sys
sys.path.append('/home/sussman/projects/effrecipes/objects')
import effrecipes


# -----------------------------------------------------------------

# Initialize database connection

conn = MySQLdb.connect(user='effuser', passwd='effuser', db='effrecipes')

# Initial generic HTML 'header' output

print "Content-type: text/html\n\n";
print "<html><head><title>Effrecipes!</title>\n"
print "<h1>Effrecipes!</h1><h2>Go ahead... change the database</h2></head>\n\n"


# Show complete list of records

print "<b>Complete List of Records:</b>\n"

print "<table border=1><tr><td>UnitID</td><td>Name</td></tr>\n"

unitlist = effrecipes.unit_list(None, conn)
for record in unitlist:
  print "<tr>"
  print '<td><a href="edit_unit.cgi?Id='+ str(record.UnitId) \
        +'">', record.UnitId, '</a></td>'
  print "<td>", record.Name, "</td>"
  print "</tr>\n"

print "</table><br/>"

print '<a href="edit_unit.cgi?Id=new">Create new record</a><br/>'


# Cleanup and exit
print "</html>"
conn.close()
