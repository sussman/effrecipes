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
  print "<html><head><title>Effrecipes:  edit record</title>\n"
  print "<center><h1>", page_title, "</h1></center></head>\n\n"

def print_footer():
  print "</html>"

def print_new_form():
  # create an empty form, all fields editable, Id will be auto-generated
  print '<form method="POST" action="RecipeSave.cgi">\n'

  print '<h2>Recipe Name:</h2><br/>'
  print '<input name="recipe_name" type="text" size="70"><br/>'

  print '<h2>Instructions:</h2><br/>'
  print '<textarea name="recipe_instructions" rows="20" cols="70">'
  print '</textarea><br/>'

  print '<h2>Commentary:</h2><br/>'
  print '<textarea name="recipe_commentary" rows="8" cols="70">'
  print '</textarea><br/>'

  print '<h2>Serving History:</h2><br/>'
  print '<textarea name="recipe_servinghistory" rows="8" cols="70">'
  print '</textarea><br/>'

  print '<h2>Attribution:</h2><br/>'
  print '<input name="recipe_attribution" type="text" size="70"><br/>'

  print '<h2>Rating (a number):</h2><br/>'
  print '<input name="recipe_rating" type="text" size="70"><br/>'

  print '<input type="submit" name="save_button" value="Save Recipe">'
  print '</form>\n'

  
def print_populated_form(Id, connection):
  # load object from the database, pre-populate form, Id not editable.
  recipe = effrecipes.recipe_lookup(Id, connection)
  
  print '<form method="POST" action="RecipeSave.cgi">\n'
  print 'Recipe Id:', recipe.RecipeId, '<br/>'
  print '<input name="recipe_id" type="hidden" value="'+ str(recipe.RecipeId)\
           + '" ><br/>'  

  print '<h2>Recipe Name:</h2><br/>'
  print '<input name="recipe_name" type="text" size="70" value="' + \
        recipe.Name + '"><br/>'

  print '<h2>Instructions:</h2><br/>'
  print '<textarea name="recipe_instructions" rows="20" cols="70">'
  print recipe.Instructions
  print '</textarea><br/>'

  print '<h2>Commentary:</h2><br/>'
  print '<textarea name="recipe_commentary" rows="8" cols="70">'
  print recipe.Commentary
  print '</textarea><br/>'

  print '<h2>Serving History:</h2><br/>'
  print '<textarea name="recipe_servinghistory" rows="8" cols="70">'
  print recipe.ServingHistory
  print '</textarea><br/>'

  print '<h2>Attribution:</h2><br/>'
  print '<input name="recipe_attribution" type="text" size="70" value="' + \
        recipe.Attribution + '"><br/>'

  print '<h2>Rating (a number):</h2><br/>'
  print '<input name="recipe_rating" type="text" size="70" value="' , \
        recipe.Rating , '"><br/>'
  
  print '<input type="submit" name="save_button" value="Save Recipe">'
  print '<input type="submit" name="delete_button" value="Delete Recipe">'
  print '</form>\n'


# Main logic
conn = MySQLdb.connect(user='effuser', passwd='effuser', db='effrecipes')

form = cgi.FieldStorage()
val = form["Id"].value   # field is either record id or 'new'

if val == 'new':
  print_header("New Recipe Details")
  print_new_form()
else:
  print_header("Edit Recipe Details")
  print_populated_form(int(val), conn)
print_footer()

conn.close()

