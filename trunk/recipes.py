#!/usr/bin/env python2

# (C) 2003 Ben Collins-Sussman under the GNU General Public License.
# See the file COPYING for details.

# A set of python classes which "encapsulate" the data objects being
# manipulated in the effrecipe database.  The fields of each class
# match the object being manipulated.  Each class has methods for
# reading/writing the object to the database.

# Create "in memory' objects... what are the use-cases?
#
#  - READ: user does a query, gets back a list of objects
#  - MODIFY: edits one object's fields, wants to overwrite existing record.
#  - CREATE: fills in all fields (but id), new record written & id created.
#
#  READ:    1. construct query, get back list of rows
#           2. convert each row into an object (all fields already present)
#           3. present list to user, each hyperlinked with an Id
#           4. create an object based on Id alone (lookup), render.
#
#  MODIFY:  1. start with an object, render fields for user
#           2. user edits fields (but Id is not editable)
#           3. object constructed from all fields, re-saved under same Id-key.
#
#  CREATE:  1. bunch of empty fields presented to user (not Id)
#           2. object constructed from all fields
#           3. save object as 'new' --> new Id created.

import MySQLdb

# Callers to this library need to create a MySQL 'connection' object,
# like so:
#
#  conn = MySQLdb.connect(user='effuser', passwd='effuser', db='effrecipes')


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
    cursor.execute(command)

  def delete(self, connection):
    """Delete object from database, keyed on its Id field."""

    command = "DELETE FROM units WHERE UnitId=" + str(self.UnitId) + ";"
    cursor = connection.cursor()
    cursor.execute(command)
    

# General 'read' interfaces which return object(s)

def unit_lookup(Id, connection):
    "Construct object by looking it up its ID."

    query = "SELECT * FROM units WHERE UnitId=" + str(Id) + ";"
    cursor = connection.cursor()
    cursor.execute(query)
    row = cursor.fetchone()  ### verify there is EXACTLY one hit!
    return Unit(row[0], row[1])


def unit_query(condition, connection):
    """Return a list of objects resulting from a table query for SQL
    CONDITION.  If CONDITION is None, return all objects."""

    query = "SELECT * FROM units"
    if (condition):
      query = query + " WHERE " + condition
    query += ";"    
    cursor = connection.cursor()
    cursor.execute(query)

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
    cursor.execute(command)

  def delete(self, connection):
    """Delete object from database, keyed on its Id field."""

    command = "DELETE FROM ingredients WHERE IngId=" + str(self.IngId) + ";"
    cursor = connection.cursor()
    cursor.execute(command)
    

# General 'read' interfaces which return object(s)

def ingredient_lookup(Id, connection):
    "Construct object by looking it up its ID."

    query = "SELECT * FROM ingredients WHERE IngId=" + str(Id) + ";"
    cursor = connection.cursor()
    cursor.execute(query)
    row = cursor.fetchone()  ### verify there is EXACTLY one hit!
    return Ingredient(row[0], row[1])


def ingredient_query(condition, connection):
    """Return a list of objects resulting from a table query for SQL
    CONDITION.  If CONDITION is None, return all objects."""

    query = "SELECT * FROM ingredients"
    if (condition):
      query = query + " WHERE " + condition
    query += ";"    
    cursor = connection.cursor()
    cursor.execute(query)

    list = []
    row = cursor.fetchone()
    while row:
      list.append(Ingredient(row[0], row[1]))
      row = cursor.fetchone()

    return list


# ------ INGREDIENT QUANTITIES -------------------------------------

# An object that represents some specific quantity of an ingredient.
# This class has no unique key;  only a non-unique RecipeId key.
class IngredientQuantity:

  def __init__(self, RecipeId, Amount, UnitId, IngId, Verb=None):
    self.RecipeId = RecipeId       # the recipe this record belongs to
    self.Amount = Amount           # a number, like "3"
    self.UnitId = UnitId           # a UnitId, like "teaspoon"
    self.IngId = IngId             # an IngredientId, like "sugar"
    self.Verb = Verb               # optional modifiers ("refined, chopped")

  def save(self, connection):
    """Save object to database.  All fields must be defined except 'Verb'."""

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
    cursor.execute(command)

  def delete(self, connection):
    """Delete object from database, keyed on its Id field."""

    command = "DELETE FROM ingredients WHERE IngId=" + str(self.IngId) + ";"
    cursor = connection.cursor()
    cursor.execute(command)
    

# General 'read' interfaces which return object(s)

def ingredient_lookup(Id, connection):
    "Construct object by looking it up its ID."

    query = "SELECT * FROM ingredients WHERE IngId=" + str(Id) + ";"
    cursor = connection.cursor()
    cursor.execute(query)
    row = cursor.fetchone()  ### verify there is EXACTLY one hit!
    return Ingredient(row[0], row[1])


def ingredient_query(condition, connection):
    """Return a list of objects resulting from a table query for SQL
    CONDITION.  If CONDITION is None, return all objects."""

    query = "SELECT * FROM ingredients"
    if (condition):
      query = query + " WHERE " + condition
    query += ";"    
    cursor = connection.cursor()
    cursor.execute(query)

    list = []
    row = cursor.fetchone()
    while row:
      list.append(Ingredient(row[0], row[1]))
      row = cursor.fetchone()

    return list


# ------ CATEGORIES ------------------------------------------------

### write someday.  low priority for the moment.


# ------ USERS -----------------------------------------------------

### write someday.  low priority for the moment.


# ------ RECIPES ---------------------------------------------------

class Recipe:

  # Constructor:  all fields already available, just assemble.
  def __init__(self, Id, Name, Rating, Instructions,
               IngredientList, Commentary, ServingHistory, Attribution):
    self.RecipeId = Id
    self.Name = Name
    self.Rating = Rating
    self.Instructions = Instructions
    self.Commentary = Commentary
    self.ServingHistory = ServingHistory
    self.Attribution = Attribution
    self.IngredientList = IngredientList  # list of IngredientQuantity objects

