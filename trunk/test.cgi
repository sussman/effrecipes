#!/usr/bin/env python2

import MySQLdb
import cgi

# utility function
def print_column(column_name, value):
    """Print a column with HTML formatting."""
    print "<strong>%s</strong>" % column_name
    print value, "<br>"


# Grab CGI information from the original HTML form

#  form = cgi.FieldStorage()
#  value = form.getvalue('formname')
#  query = 'SELECT * FROM effrecipes where ('
#  query += '______'

# testing... 1, 2, 3

query = "SHOW TABLES;"

# Connect to MySQL, and run the query:
conn = MySQLdb.connect(user='effuser', passwd='effuser', db='effrecipes')
cursor = conn.cursor()
cursor.execute(query)



print "Content-type: text/html\n\n";

print "<html>"
print "<h3>Found %d tables in the database:</h3>" % cursor.rowcount


row = cursor.fetchone()
while row:
  if row[0]:
    print_column ('Table Name:', row[0])
  row = cursor.fetchone()

# Close the MySQL connection.
conn.close()

print "</html>"
