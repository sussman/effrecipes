#!/usr/bin/env python2

# Generate an HTML front-page for the Effrecipe Database 

import MySQLdb, cgi, recipes

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

unitlist = recipes.unit_query(None, conn)
for record in unitlist:
  print "<tr>"
  print '<td><a href="edit_unit.cgi">', record.UnitId, '</a></td>'
  print "<td>", record.Name, "</td>"
  print "</tr>\n"

print "</table>"


# Cleanup and exit
print "</html>"
conn.close()
