#!/usr/bin/env python2

# (C) 2003 Ben Collins-Sussman under the GNU General Public License.
# See the file COPYING for details.

# Edit a "Unit" record.

import MySQLdb, cgi, recipes

# enable debugging:  displays detailed exceptions in web browser.
import cgitb; cgitb.enable()

# -----------------------------------------------------------------

def save_record(form, conn):
  
  name = form["unit_name"].value
  if form.has_key("unit_id"):
    id = int(form["unit_id"].value)  # will edit existing record
  else:
    id = None  # will create new record
    
    unit_object = recipes.Unit(id, name)
    unit_object.save(conn)
    
    if id != None:
      print "Record with Id ", form["unit_id"].value, "has been saved.<br/>\n"
    else:
      print "New record created.<br/>"

def delete_record(form, conn):

  name = form["unit_name"].value
  id = int(form["unit_id"].value)
  
  unit_object = recipes.Unit(id, name)
  unit_object.delete(conn)
  
  print "Record deleted.<br/>"

# -----------------------------------------------------------------

# Initialize database connection
conn = MySQLdb.connect(user='effuser', passwd='effuser', db='effrecipes')

# Initial generic HTML 'header' output
print "Content-type: text/html\n\n";
print "<html><head><title>Effrecipes - record changed</title>\n"
print "<h2>Changed record.</h2></head>\n\n"

# Use the CGI form values to create a new object and save it.
form = cgi.FieldStorage()

if form.has_key("save_button"):
  save_record(form, conn)
elif form.has_key("delete_button"):
  delete_record(form, conn)
else:
  print "Unknown action -- no button recognized"

print '<a href="frontpage.cgi">Go back to the front page</a>.\n'

# Cleanup and exit
print "</html>"
conn.close()

