from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from effrecipes.recipes.models import *

# From the tutorial: every URL callback must either return an
# HttpResponse object containing page content, or must raise an http
# exception.


# Front page of site
def index(request):
  num_recipes = Recipe.objects.count()
  cats = RecipeCategory.objects.filter(is_primary__exact=True)
  return render_to_response('frontpage.html', {'recipecount' : num_recipes,
                                               'cats' : cats })


# Function which processes a search request from the front page (via POST)
def recipe_search(request):
  term = request.POST['searchtext']

  # search for the term in Recipe fields first
  recipes = Recipe.objects.filter(
    Q(title__contains=term)
    | Q(instructions__contains=term)
    | Q(servinghistory__contains=term)
    | Q(attribution__contains=term)
    )

  # Then search through Ingredients
  ingredients = Ingredient.objects.filter(
    Q(unit__id__contains=term)
    | Q(food__id__contains=term)
    | Q(verb__contains=term)
    )
  for ing in ingredients:
    r = ing.recipe
    if r not in recipes:
      recipes.append(r)

  return render_to_response('searchresults.html', { 'recipes' : recipes } )


# Display all recipes within a category
def show_category(request, category_id):
  recipes = Recipe.objects.filter(categories__id__exact=category_id)
  return render_to_response('searchresults.html', { 'recipes' : recipes } )


# Read-only view of a single recipe
def detail(request, recipe_id):
  r = get_object_or_404(Recipe, pk=recipe_id)
  ings = Ingredient.objects.filter(recipe__id__exact=recipe_id)
  cats = RecipeCategory.objects.filter(recipes__exact=recipe_id)
  return render_to_response('details.html', {'recipe' : r,
                                             'inglist' : ings,
                                             "catlist" : cats} )

