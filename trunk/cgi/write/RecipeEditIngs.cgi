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


def print_form(recipe, conn):
  # fetch the lists of all known units and ingredients
  all_units = effrecipes.unit_list(None, conn)
  all_ingredients = effrecipes.ingredient_list(None, conn)

  # fetch the current list of IngredientQuantity objects attached to recipe
  current_ingredients = recipe.ingredientlist(conn)

  # the form action invokes this same page again, so users can
  # repeatedly add ingredients.
  print '<form method="POST" action="RecipeEditIngs.cgi">\n'
  print '<input name="Id" type="hidden" value="'+str(recipe.RecipeId)+'" >'
  
  print 'Numerical quantity: <input name="Amount" type="text">'

  print 'Unit: <select name="UnitId">'
  for record in all_units:
    print '<option value="'+str(record.UnitId)+ '">'+record.Name+"</option>"
  print '</select>'

  print 'Ingredient: <select name="IngId">'
  for record in all_ingredients:
    print '<option value="'+str(record.IngId)+ '">'+record.Name+"</option>"
  print '</select>\n'


  print '<input type="submit" name="add_button" value="Add ingredient">'
  print '</form>\n'

  # show all attached IngredientQuantity objects in a table, with option
  # to delete any one of them.
  
  print '<h3>Current ingredients attached to this recipe:</h3>'
  print "<table border=1>\n"
  for record in current_ingredients:
    unit = effrecipes.unit_lookup(record.UnitId, conn)
    ingredient = effrecipes.ingredient_lookup(record.IngId, conn)

    print '<tr>'
    print '<td>Amount = ' + str(record.Amount) + '</td>'
    print '<td>' + unit.Name + '</td>'
    print '<td>' + ingredient.Name + '</td>'
    print '<td><form>'
    print '<input type="submit" name="delete_button" value="Delete">'
    print '</form></td>'
    print '</tr><br/>'
  print "</table><br/>"


#------------------------------------------------------------------------
# Main logic

conn = MySQLdb.connect(user='effuser', passwd='effuser', db='effrecipes')
form = cgi.FieldStorage()

# fetch the recipe object to which we're attaching ingredients
val = form["Id"].value
recipe = effrecipes.recipe_lookup(int(val), conn)

# Initial handshake output
print_header("Adding Ingredients to <br/>'" + recipe.Name + "'")

# Accepting new data:
#    There MIGHT be new ingredientquantity data coming in here;
#    if so, validate it and create a new record.
if (form.has_key("Amount")):
  amount = int(form["Amount"].value)
  unitid = int(form["UnitId"].value)
  ingid = int(form["IngId"].value)
  new_ingquantity = effrecipes.IngredientQuantity(int(val),
                                                  amount, unitid, ingid)
  new_ingquantity.save(conn)

# Now show the real input form
print_form(recipe, conn)
print_footer()

conn.close()

