#!/usr/bin/env python2

# (C) 2003 Ben Collins-Sussman under the GNU General Public License.
# See the file COPYING for details.

# A set of python classes which "encapsulate" the data objects being
# manipulated in the effrecipe database.  The fields of each class
# match the object being manipulated.  Each class has methods for
# reading/writing the object to the database.


# Here is the basic API for database records that have unique ID keys:
#
#  class foo:
#     foo(ID):          constructor builds object *in memory) with unique ID.
#     foo.save():       write in-memory object to database table.
#     foo.delete():     delete in-memory object from database table.
#
#  foo_lookup(ID):      read database, return specific in-memory object
#  foo_list(condition): query database, return list of matching objects


import MySQLdb

# Callers to this library need to create a MySQL 'connection' object,
# like so:
#
#  conn = MySQLdb.connect(user='effuser', passwd='effuser', db='effrecipes')


# ----- DB COMMANDS -------------------------------------------------

# It's much easier to debug the SQL commands we execute if they're
# appended to a logfile.  Here's a wrapper for that.

logfile = "/home/sussman/projects/effrecipes/sql_log"  ### generalize this

def run_sql(command, cursor):
  "Use db cursor to execute sql command, logging command to a file first."
  fp = open(logfile, 'a')  # open in (a)ppend mode
  fp.write(command + "\n")
  fp.close()
  cursor.execute(command)


# ------ UNITS -------------------------------------------------------

# a basic unit of measure.  the db table is just a name and unique id.
class Unit:

  # Constructor:  all fields already available, just assemble.
  # Pass "None" for Id if this is a new object, not yet saved.
  def __init__(self, Id, Name):
    self.UnitId = Id
    self.Name = Name

  def save(self, connection):
    """Save object to database, keyed on its Id field.  If object's Id
    field is defined, then overwrite existing record.  Else create new
    record for Id."""

    if (self.UnitId):
      fields = "Name='" + self.Name + "'"
      command = "UPDATE units SET " + fields + " WHERE UnitId=" \
                + str(self.UnitId) + ";"

    else:
      # by not mentioning the Id field, it should auto-increment.
      fields = "(Name)"
      values = "(" + "'" + self.Name + "'" + ")"
      command = "INSERT INTO units " + fields + " VALUES " + values + ";"

    cursor = connection.cursor()
    run_sql(command, cursor)


  def delete(self, connection):
    """Delete object from database, keyed on its Id field."""

    command = "DELETE FROM units WHERE UnitId=" + str(self.UnitId) + ";"
    cursor = connection.cursor()
    run_sql(command, cursor)
    

# General 'read' interfaces which return object(s)

def unit_lookup(Id, connection):
    "Construct object by looking it up its ID."

    query = "SELECT * FROM units WHERE UnitId=" + str(Id) + ";"
    cursor = connection.cursor()
    run_sql(query, cursor)
    row = cursor.fetchone()  ### verify there is EXACTLY one hit!
    return Unit(row[0], row[1])


def unit_list(condition, connection):
    """Return a list of objects resulting from a table query for SQL
    CONDITION.  If CONDITION is None, return all objects."""

    query = "SELECT * FROM units"
    if (condition):
      query = query + " WHERE " + condition
    query += ";"    
    cursor = connection.cursor()
    run_sql(query, cursor)

    list = []
    row = cursor.fetchone()
    while row:
      list.append(Unit(row[0], row[1]))
      row = cursor.fetchone()

    return list
  

# ------ INGREDIENTS -------------------------------------------------

# a basic ingredient.  the db table is nothing but a name and unique id.
class Ingredient:
  
  # Constructor:  all fields already available, just assemble.
  # Pass "None" for Id if this is a new object, not yet saved.
  def __init__(self, Id, Name):
    self.IngId = Id
    self.Name = Name

  def save(self, connection):
    """Save object to database, keyed on its Id field.  If object's Id
    field is defined, then overwrite existing record.  Else create new
    record for Id."""

    if (self.IngId):
      fields = "Name='" + self.Name + "'"
      command = "UPDATE ingredients SET " + fields + " WHERE IngId=" \
                + str(self.IngId) + ";"

    else:
      # by not mentioning the Id field, it should auto-increment.
      fields = "(Name)"
      values = "(" + "'" + self.Name + "'" + ")"
      command = "INSERT INTO ingredients " + fields + " VALUES " + values + ";"

    cursor = connection.cursor()
    run_sql(command, cursor)


  def delete(self, connection):
    """Delete object from database, keyed on its Id field."""

    command = "DELETE FROM ingredients WHERE IngId=" + str(self.IngId) + ";"
    cursor = connection.cursor()
    run_sql(command, cursor)

    

# General 'read' interfaces which return object(s)

def ingredient_lookup(Id, connection):
    "Construct object by looking it up its ID."

    query = "SELECT * FROM ingredients WHERE IngId=" + str(Id) + ";"
    cursor = connection.cursor()
    run_sql(query, cursor)
    row = cursor.fetchone()  ### verify there is EXACTLY one hit!
    return Ingredient(row[0], row[1])


def ingredient_list(condition, connection):
    """Return a list of objects resulting from a table query for SQL
    CONDITION.  If CONDITION is None, return all objects."""

    query = "SELECT * FROM ingredients"
    if (condition):
      query = query + " WHERE " + condition
    query += ";"    
    cursor = connection.cursor()
    run_sql(query, cursor)

    list = []
    row = cursor.fetchone()
    while row:
      list.append(Ingredient(row[0], row[1]))
      row = cursor.fetchone()

    return list


# ------ INGREDIENT QUANTITIES -------------------------------------

# An object that represents some specific quantity of an ingredient.
#   - For example:  "3 teaspoons sugar, confectioner's"
#   - Each record in this table is attached to a recipe;  in other words,
#     every recipe has a list of ingredient-quantity records.
#   - This class has no unique key;  only a non-unique RecipeId key.

class IngredientQuantity:

  def __init__(self, RecipeId, Amount, UnitId, IngId, Verb=None):
    self.RecipeId = RecipeId       # the recipe this record belongs to
    self.Amount = Amount           # a number, like "3"
    self.UnitId = UnitId           # a UnitId, like "teaspoon"
    self.IngId = IngId             # an IngredientId, like "sugar"
    self.Verb = Verb               # optional modifiers ("refined, chopped")

  # Because a record in this table has no unique ID field, the only
  # way to find a specific record is to construct a WHERE clause based
  # on the object's fields:
  def where_clause(self):
    """Return a SQL 'WHERE' string that uniquely identifies this object,
    used for reading or deleting."""
    command = " WHERE "
    command += "RecipeId=" + str(self.RecipeId)
    command += "and Amount=" + str(self.Amount)
    command += "and UnitId=" + str(self.UnitId)
    command += "and IngId=" + str(self.IngId)
    if (self.Verb is None):
      command += "and Verb is NULL"
    else:
      command += "and Verb='" + self.Verb + "'"
    command += ";"

  def toString(self, connection):
    """Return a string which describes the ingredientquantity"""
    unit = unit_lookup(self.UnitId, connection)
    ingredient = ingredient_lookup(self.IngId, connection)
    string = str(self.Amount) + " " + unit.Name + " " \
             + ingredient.Name + " " + self.Verb
    return string

  def save(self, connection):
    """Save object to database.  All fields must be defined except 'Verb'."""

    command = "INSERT INTO ingredient_quantities "
    command += "(RecipeId, Amount, UnitId, IngID"
    if (self.Verb is not None):
      command += ", Verb"
    command += ") VALUES ("
    command += str(self.RecipeId) + "," + str(self.Amount) + ","
    command += str(self.UnitId) + "," + str(self.IngId)
    if (self.Verb is not None):
      command += "," + str(self.Verb)
    command += ")"
    print "command is: ", command
    cursor = connection.cursor()
    run_sql(command, cursor)

  def delete(self, connection):
    """Delete object from database, keyed on ALL its fields."""
    
    command = "DELETE FROM ingredient_quantities " + self.where_clause()
    cursor = connection.cursor()
    run_sql(command, cursor)

    

# General 'read' interfaces which return object(s)

def ingredientquantity_lookup(Id, connection):
    "Construct object by looking it up, keyed on ALL its fields."

    query = "SELECT * FROM ingredient_quantities " + self.where_clause()
    cursor = connection.cursor()
    run_sql(query, cursor)
    row = cursor.fetchone()
    return IngredientQuantity(row[0], row[1], row[2], row[3], row[4])


def ingredientquantity_query(condition, connection):
    """Return a list of objects resulting from a table query for SQL
    CONDITION.  If CONDITION is None, return all objects."""

    query = "SELECT * FROM ingredient_quantities"
    if (condition):
      query = query + " WHERE " + condition
    query += ";"    
    cursor = connection.cursor()
    run_sql(query, cursor)

    list = []
    row = cursor.fetchone()
    while row:
      list.append(IngredientQuantity(row[0], row[1], row[2], row[3], row[4]))
      row = cursor.fetchone()

    return list


# ------ CATEGORIES ------------------------------------------------

### write someday.  low priority for the moment.


# ------ USERS -----------------------------------------------------

### write someday.  low priority for the moment.


# ------ RECIPES ---------------------------------------------------

class Recipe:

  # Constructor:  all fields already available, just assemble.
  # Pass "Id=None" if this is a new object, not yet saved.
  def __init__(self, Id, Name, Rating, Instructions,
               Commentary, ServingHistory, Attribution):
    self.RecipeId = Id
    self.Name = Name
    self.Rating = Rating
    self.Instructions = Instructions
    self.Commentary = Commentary
    self.ServingHistory = ServingHistory
    self.Attribution = Attribution

  def ingredientlist(self, connection):
    "Return list of all IngredientQuantity records attached to recipe."

    condition = "RecipeId='" + str(self.RecipeId)  + "'" 
    return ingredientquantity_query(condition, connection)

  def save(self, connection):
    """Save object to database, keyed on its Id field.  If object's Id
    field is defined, then overwrite existing record.  Else create new
    record for Id."""

    if (self.RecipeId):
      fields = "Name='" + self.Name + "',"
      fields += "Rating='" + str(self.Rating) + "',"
      fields += "Instructions='" + self.Instructions + "',"
      fields += "Commentary='" + self.Commentary + "',"
      fields += "ServingHistory='" + self.ServingHistory + "',"
      fields += "Attribution='" + self.Attribution + "' "
      command = "UPDATE recipes SET " + fields + " WHERE RecipeId=" \
                + str(self.RecipeId) + ";"

    else:
      # by not mentioning the Id field, it should auto-increment.
      fields = "(Name, Rating, Instructions, "
      fields += " Commentary, ServingHistory, Attribution)"
      values = "(" + "'" + self.Name + "', "
      values += "'" + str(self.Rating) + "', "
      values += "'" + self.Instructions + "', "
      values += "'" + self.Commentary + "', "
      values += "'" + self.ServingHistory + "', "
      values += "'" + self.Attribution + "'"
      values += ")"
      command = "INSERT INTO recipes " + fields + " VALUES " + values + ";"

    cursor = connection.cursor()
    run_sql(command, cursor)


  def delete(self, connection):
    """Delete object from database, keyed on its Id field."""

    command = "DELETE FROM recipes WHERE RecipeId=" + str(self.RecipeId) + ";"
    cursor = connection.cursor()
    run_sql(command, cursor)

    

# General 'read' interfaces which return object(s)

def recipe_lookup(Id, connection):
    "Construct object by looking it up its ID."

    query = "SELECT * FROM recipes WHERE RecipeId=" + str(Id) + ";"
    cursor = connection.cursor()
    run_sql(query, cursor)
    row = cursor.fetchone()  ### verify there is EXACTLY one hit!
    return Recipe(row[0], row[1], row[2], row[3], row[4], row[5], row[6])


def recipe_list(condition, connection):
    """Return a list of objects resulting from a table query for SQL
    CONDITION.  If CONDITION is None, return all objects."""

    query = "SELECT * FROM recipes"
    if (condition):
      query = query + " WHERE " + condition
    query += ";"    
    cursor = connection.cursor()
    run_sql(query, cursor)

    list = []
    row = cursor.fetchone()
    while row:
      list.append(Recipe(row[0], row[1], row[2], \
                         row[3], row[4], row[5], row[6]))
      row = cursor.fetchone()

    return list
