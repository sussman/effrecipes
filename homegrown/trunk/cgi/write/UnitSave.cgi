#!/usr/bin/env python2

# (C) 2003 Ben Collins-Sussman under the GNU General Public License.
# See the file COPYING for details.

# Edit a "Unit" record.

import MySQLdb, cgi

# enable debugging:  displays detailed exceptions in web browser.
import cgitb; cgitb.enable()

# temporary:  eventually put 'effrecipes.py' into a standard PYTHONPATH
# location, like /usr/lib/python2.3/site-pacakages/
import sys
sys.path.append('/home/sussman/projects/effrecipes/objects')
import effrecipes


# -----------------------------------------------------------------

def save_record(form, conn):
  """Write record in FORM to database, overwriting unit with
  matching Id field..  If FORM has no Id field, a new record is
  created in database."""

  name = form["unit_name"].value
  if form.has_key("unit_id"):
    id = int(form["unit_id"].value)
  else:
    id = None

  # This will either read an existing record (if id is an integer),
  # or create a new record (if id is None)
  unit_object = effrecipes.Unit(id, name)
  unit_object.save(conn)
    
  if id is None:
    print "New record created.<br/>"
  else:    
    print "Record with Id ", form["unit_id"].value, "has been saved.<br/>\n"


def delete_record(form, conn):
  "Delete record that matches FORM's Id."

  name = form["unit_name"].value
  id = int(form["unit_id"].value)
  
  unit_object = effrecipes.Unit(id, name)
  unit_object.delete(conn)
  
  print "Record deleted.<br/>"

# -----------------------------------------------------------------

# Initialize database connection
conn = MySQLdb.connect(user='effuser', passwd='effuser', db='effrecipes')

# Initial generic HTML 'header' output
print "Content-type: text/html\n\n";
print "<html><head><title>Effrecipes - record has changed</title>\n"

# Use the CGI form values to create a new object and save it.
form = cgi.FieldStorage()

if form.has_key("save_button"):
  save_record(form, conn)
elif form.has_key("delete_button"):
  delete_record(form, conn)
else:
  print "Unknown action -- no button recognized"

print 'Go back to the <a href="../read/UnitListDisplay.cgi">'\
      + 'list of all Units.</a>.\n'

# Cleanup and exit
print "</html>"
conn.close()

