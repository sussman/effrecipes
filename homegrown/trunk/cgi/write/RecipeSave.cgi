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

  if form.has_key("recipe_id"):
    id = int(form["recipe_id"].value)
  else:
    id = None

  name = form["recipe_name"].value
  instructions = form["recipe_instructions"].value
  commentary = form["recipe_commentary"].value
  servinghistory = form["recipe_servinghistory"].value
  attribution = form["recipe_attribution"].value
  rating = form["recipe_rating"].value
  
  # This will either read an existing record (if id is an integer),
  # or create a new record (if id is None)
  recipe_object = effrecipes.Recipe(id, name, rating, instructions, \
                                    commentary, servinghistory, attribution)
  recipe_object.save(conn)
    
  if id is None:
    print "New recipe saved.<br/>"
  else:    
    print "Recipe #", form["recipe_id"].value, "has been updated.<br/>\n"


def delete_record(form, conn):
  "Delete record that matches FORM's Id."

  id = int(form["recipe_id"].value)  
  recipe = effrecipes.recipe_lookup(id, conn)
  recipe.delete(conn)
  
  print "Recipe deleted.<br/>"

# -----------------------------------------------------------------

# Initialize database connection
conn = MySQLdb.connect(user='effuser', passwd='effuser', db='effrecipes')

# Initial generic HTML 'header' output
print "Content-type: text/html\n\n";
print "<html><head><title>Effrecipes - recipe has changed</title>\n"

# Use the CGI form values to create a new object and save it.
form = cgi.FieldStorage()

if form.has_key("save_button"):
  save_record(form, conn)
elif form.has_key("delete_button"):
  delete_record(form, conn)
else:
  print "Unknown action -- no button recognized"

print 'Go back to the <a href="../read/RecipeListDisplay.cgi">'\
      + 'list of all Recipes.</a>.\n'

# Cleanup and exit
print "</html>"
conn.close()

