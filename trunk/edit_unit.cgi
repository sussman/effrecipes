#!/usr/bin/env python2

# (C) 2003 Ben Collins-Sussman under the GNU General Public License.
# See the file COPYING for details.

# Edit a "Unit" record.

import MySQLdb, cgi, recipes

# enable debugging:  displays detailed exceptions in web browser.
import cgitb; cgitb.enable()

# -----------------------------------------------------------------

def print_header(page_title):
  print "Content-type: text/html\n\n";
  print "<html><head><title>Effrecipes</title>\n"
  print "<h2>", page_title, "</h2></head>\n\n"

def print_footer():
  print "</html>"

def print_new_form():
  # create an empty form, all fields editable, Id will be auto-generated
  print '<form method="POST" action="save_unit.cgi">\n'
  print 'Enter new name:<br/>'
  print '<input name="unit_name" type="text"><br/>'
  print '<input type="submit" name="save_button" value="Save Record">'
  print '</form>\n'
  
def print_populated_form(Id, connection):
  # load object from the database, pre-populate form, Id not editable.
  unit = recipes.unit_lookup(Id, connection)
  
  print '<form method="POST" action="save_unit.cgi">\n'
  print 'Record Id:', unit.UnitId, '<br/>'
  print '<input name="unit_id" type="hidden" value="'+ str(unit.UnitId)\
           + '" ><br/>'  
  print 'Change the name:<br/>'
  print '<input name="unit_name" type="text" value="'+ unit.Name + '" ><br/>'
  print '<input type="submit" name="save_button" value="Save Record">'
  print '<input type="submit" name="delete_button" value="Delete Record">'
  print '</form>\n'


# Main logic
conn = MySQLdb.connect(user='effuser', passwd='effuser', db='effrecipes')

form = cgi.FieldStorage()
val = form["Id"].value   # field is either record id or 'new'

print_header("Editing a 'Unit' Record")
if val == 'new':
  print_new_form()
else:
  print_populated_form(int(val), conn)
print_footer()

conn.close()

