#!/usr/bin/env python2

import MySQLdb
import cgi


# Grab CGI information from the original HTML form

#  form = cgi.FieldStorage()
#  value = form.getvalue('formname')
#  query = 'SELECT * FROM effrecipes where ('
#  query += '______'

# testing... 1, 2, 3

query = "describe ingredient_lists;"

# Connect to MySQL, and run the query:
conn = MySQLdb.connect(user='effuser', passwd='effuser', db='effrecipes')
cursor = conn.cursor()
cursor.execute(query)

print "Content-type: text/html\n\n";

print "<html>"
print "<h3>Found %d results:</h3>" % cursor.rowcount


row = cursor.fetchone()
while row:
  for item in row:
    print item, ":",
  print "<br/>\n"
  row = cursor.fetchone()

# Close the MySQL connection.
conn.close()

print "</html>"
