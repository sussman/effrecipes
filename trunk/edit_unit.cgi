#!/usr/bin/env python2

# (C) 2003 Ben Collins-Sussman under the GNU General Public License.
# See the file COPYING for details.

# Edit a "Unit" record.

import MySQLdb, cgi, recipes

# enable debugging:  displays detailed exceptions in web browser.
import cgitb; cgitb.enable()

# -----------------------------------------------------------------

# Initialize database connection
conn = MySQLdb.connect(user='effuser', passwd='effuser', db='effrecipes')

# Initial generic HTML 'header' output
print "Content-type: text/html\n\n";
print "<html><head><title>Effrecipes - edit record</title>\n"
print "<h2>Editing a record...</h2></head>\n\n"

# Parse the CGI querystring... should either be "new" or an Id number.
form = cgi.FieldStorage()
q = form["Id"].value

print '<form method="POST" action="save_unit.cgi">\n'

if q == 'new':
  # create an empty form, all fields editable, Id will be auto-generated
  print 'Enter new name:<br/>'
  print '<input name="unit_name" type="text"><br/>'

else:
  # load object from the database, pre-populate form, Id not editable.
  q = int(q)

  unit = recipes.unit_lookup(int(q), conn)

  print 'Record Id:', unit.UnitId, '<br/>'
  print '<input name="unit_id" type="hidden" value="'+ str(unit.UnitId) + '" ><br/>'
  
  print 'Change the name:<br/>'
  print '<input name="unit_name" type="text" value="'+ unit.Name + '" ><br/>'

print '<input type="submit" name="save_button" value="Save Record">'

print '<input type="submit" name="delete_button" value="Delete Record">'

print '</form>\n'

# Cleanup and exit
print "</html>"
conn.close()

