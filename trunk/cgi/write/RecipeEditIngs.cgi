#!/usr/bin/env python2

# (C) 2003 Ben Collins-Sussman under the GNU General Public License.
# See the file COPYING for details.


import MySQLdb, cgi

# enable debugging:  displays detailed exceptions in web browser.
import cgitb; cgitb.enable()

# temporary:  eventually put 'effrecipes.py' into a standard PYTHONPATH
# location, like /usr/lib/python2.3/site-packages/
import sys
sys.path.append('/home/sussman/projects/effrecipes/objects')
import effrecipes


# -----------------------------------------------------------------

def print_header(page_title):
  print "Content-type: text/html\n\n";
  print "<html><head><title>Effrecipes:  add ingredient</title>\n"
  print "<center><h1>", page_title, "</h1></center></head>\n\n"

def print_footer():
  print "</html>"

def print_form(RecipeId, connection):
  print '<form method="POST" action="RecipeAddIng.cgi">\n'

  print '<input type="submit" name="add_button" value="Add ingredient">'
  print '</form>\n'



# Main logic
conn = MySQLdb.connect(user='effuser', passwd='effuser', db='effrecipes')

form = cgi.FieldStorage()
val = form["Id"].value   # Id is the RecipeId to attach ingredient to

print_header("Add Recipe Ingredient")
print_form(int(val), conn)
print_footer()

conn.close()

