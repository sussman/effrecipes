#!/usr/bin/env python2

# A set of python classes which "encapsulate" the data objects being
# manipulated in the effrecipe database.  The fields of each class
# match the object being manipulated.  Each class has methods for
# reading/writing the object to the database.


# a basic unit of measure.  the db table is just a name and unique id.
class Unit:

  def __init__(self, Name, UnitId=-1):
    self.Name = Name
    if UnitId == -1:
      # if user didn't pass an Id, try to look one up based on name
      self.UnitId = self.id_from_name(self, Name)

  def id_from_name(self, Name):
    """Look up the name of the unit in the db, return unique id
    number.  If not found, return -1."""

  def write_new_unit(self, Name):
    """Write a new unit kind to the db, return new unique id."""


# utility function:  get list of ALL unique ingredients in db
def get_all_ingredients():
  pass
  ### run a sql query, build an Ingredient object for each hit.


# a basic ingredient.  the db table is nothing but a name and unique id.
class Ingredient:

  def __init__(self, Name, IngId=-1):
    self.Name = Name
    if IngId == -1:
      # if user didn't pass an Id, try to look one up based on name
      self.IngId = self.id_from_name(self, Name)

  def id_from_name(self, Name):
    """Look up the name of the ingredient in the db, return unique id
    number.  If not found, return -1."""

  def write_new_ingredient(self, Name):
    """Write a new ingredient kind to the db, return new unique id."""


# utility function:  get list of ALL unique ingredients in db
def get_all_ingredients():
  pass
  ### run a sql query, build an Ingredient object for each hit.



# an object that represents some specific quantity of an ingredient.
class IngredientQuantity:

  def __init__(self, Amount, Unit, Ingredient, Verb=None):
    self.Amount = Amount           # a number, like "3"
    self.Unit = Unit               # a Unit object, like "teaspoon"
    self.Ingredient = Ingredient   # an Ingredient object, like "sugar"
    self.Verb = Verb               # optional, like "refined"


class Recipe:

  # presumably the constructor is called when all the data is coming
  # from a human source, like a huge CGI form.
  
  def __init__(self, Name, Rating=None, Instructions=None,
               IngredientList = [],
               Commentary=None, ServingHistory=None, Attribution=None):
    self.RecipeId = -1  # unknown/invalid id
    self.Name = Name
    self.Rating = Rating
    self.Instructions = Instructions
    self.Commentary = Commentary
    self.ServingHistory = ServingHistory
    self.Attribution = Attribution
    self.IngredientList = IngredientList  # list of IngredientQuantity objects
    

    

  
