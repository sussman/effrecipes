#!/usr/bin/env python2


import cgi

# enable debugging:  displays detailed exceptions in web browser.
import cgitb; cgitb.enable()

import MySQLdb

# temporary:  eventually put 'effrecipes.py' into a standard PYTHONPATH
# location, like /usr/lib/python2.3/site-packages/
import sys
sys.path.append('/home/sussman/projects/effrecipes/objects')
import effrecipes


# -----------------------------------------------------------------

# Initialize database connection

conn = MySQLdb.connect(user='effuser', passwd='effuser', db='effrecipes')

# Grab the object from the database

form = cgi.FieldStorage()
val = form["Id"].value   # this better be a valid ID
recipe = effrecipes.recipe_lookup(int(val), conn)
recipe_ingredients = recipe.ingredientlist(conn)

# Initial generic HTML 'header' output

print "Content-type: text/html\n\n";
print "<html><head><title>Effrecipes -- Recipe Display</title>\n"
print '<h1>Recipe: "' + recipe.Name + '"</h1></head>\n\n'

# Show ingredient list

print '<h2>Ingredients</h2>'
print '<h3><a href="../write/RecipeEditIngs.cgi?Id=' + str(recipe.RecipeId) \
        +'">(Add an ingredient)</a></h3>'


print '<h3>'
for record in recipe_ingredients:  # a bunch of IngredientQuantity records
  print record.toString(), '<br/>'
print "</h3><br/>"

# Show the recipe record itself

print '<h2>Details</h2>'
print '<h3><a href="../write/RecipeEdit.cgi?Id=' + str(recipe.RecipeId) \
        +'">(Change these details)</a></h3>'

print '<table border=1>\n'

print '<tr><td>Recipe ID</td> <td>', recipe.RecipeId, '</td></tr>'

print '<tr><td>Name</td> <td>' + recipe.Name + '</td></tr>'

print '<tr><td>Rating</td> <td>', recipe.Rating, '</td></tr>'

print '<tr><td>Instructions</td> <td>' + recipe.Instructions + '</td></tr>'

print '<tr><td>Commentary</td> <td>' + recipe.Commentary + '</td></tr>'

print '<tr><td>Serving History</td> <td>' + recipe.ServingHistory \
      + '</td></tr>'

print '<tr><td>Attribution</td> <td>' + recipe.Attribution + '</td></tr>'

print "</table><br/>"


# Cleanup and exit
print "</html>"
conn.close()
