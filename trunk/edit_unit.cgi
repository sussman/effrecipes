#!/usr/bin/env python2

# Edit a "Unit" record.

import MySQLdb, cgi, recipes

# -----------------------------------------------------------------

# Initialize database connection

conn = MySQLdb.connect(user='effuser', passwd='effuser', db='effrecipes')

# Initial generic HTML 'header' output

print "Content-type: text/html\n\n";
print "<html><head><title>Effrecipes - edit record</title>\n"
print "<h2>Editing a record...</h2></head>\n\n"


# Parse the CGI querystring... should either be "new" or an Id number.
q = '1'

print '<form>\n'

if q == 'new':
  # create an empty form, all fields editable, Id will be auto-generated
  print 'Enter new name:<br/>'
  print '<input name="unit_name" type="text">'

else:
  # load object from the database, pre-populate form, Id not editable.
  unit = recipes.unit_lookup(int(q), conn)

  # hidden Id field will tell CGI script which record is being edited
  print '<input name="unit_id" type="hidden" value="', unit.UnitId, '">'

  print 'Change the name:<br/>'
  print '<input name="unit_name" type="text" value="', unit.Name, '">'

print '</form>\n'

# Cleanup and exit
print "</html>"
conn.close()

