from django.db import models

# Data Models for Database of Cookbook Recipes.


# Categories of recipes: breads, appetizers, desserts, soups, etc.  A
# recipe can be a member of many categories, so it's a many-to-many
# relationship.

class RecipeCategory(models.Model):
  name = models.CharField('Recipe Category', maxlength=200)

  def __str__(self):
    return self.name

  class Admin:
    pass


# Types of food in a recipe (bananas, flour, cheese, tomatoes, etc.)
# This is broken out specifically so that we can compile shopping
# lists for sets of selected recipes.  Another many-to-many relationship.

class Food(models.Model):
  name = models.CharField('Food', maxlength=200)

  def __str__(self):
    return self.name

  class Admin:
    pass


# Types of units in the system (cups, teaspoons, etc.)  Another
# many-to-many relationship.

class Unit(models.Model):
  name = models.CharField('Measurement Unit', maxlength=200)

  def __str__(self):
    return self.name

  class Admin:
    pass


# Main recipe object, to glue it all together.

class Recipe(models.Model):
  # Top-level metadata
  title = models.CharField('Recipe Title', maxlength=200)
  attribution = models.CharField('Attribution', maxlength=200)
  servings = models.IntegerField('Number of Servings')
  preptime = models.IntegerField('Preparation Time (minutes)')
  categories = models.ManyToManyField(RecipeCategory)

  # Main meat (includes ingredient listing!)
  instructions = models.TextField('Instructions')

  # Other metadata
  pub_date = models.DateTimeField('Date Published')
  servinghistory = models.TextField('Serving History')
  effrating = models.IntegerField('Numerical Rating')
  comments = models.TextField('Commentary')

  # TODO:  add other fields someday:
  #   photo
  #   users attach comments to recipes

  def __str__(self):
    return self.title

  class Admin:
    pass
    fields = (
      (None, {'fields': ('title', 'attribution', 'servings',
                         'preptime', 'categories')}),
      ('Recipe Details', {'fields': ('instructions',)}),
      ('Commentary', {'fields': ('pub_date', 'servinghistory',
                                 'effrating', 'comentary')}),
      )


# These are the actual objects that get attached to recipes, as a many
# to one relationship.  Example: "3 cups spinach, chapped".

# Someday we hope to write a feature which adds recipe ingredients
# together to generate grocery shopping lists.

class Ingredient(models.Model):
  quantity = models.FloatField('Amount', max_digits=5, decimal_places=2)
  unit = models.ForeignKey(Unit)
  food = models.ForeignKey(Food, core=True)
  verb = models.CharField('Verb', maxlength=200, blank=True)
  recipe = models.ForeignKey(Recipe, edit_inline=models.TABULAR)

  def __str__(self):
    if self.verb is not None:
      return "%d %s %s, %s" % (self.quantity, self.unit, self.food, self.verb)
    else:
      return "%d %s %s" % (self.quantity, self.unit, self.food)

  class Admin:
    pass

