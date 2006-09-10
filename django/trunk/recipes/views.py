from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from effrecipes.recipes.models import *

# From the tutorial: every URL callback must either return an
# HttpResponse object containing page content, or must raise an http
# exception.


# Front page of site
def index(request):
  return HttpResponse("Hello, this is Eff's Recipe Collection.")


# Read-only view of a single recipe
def detail(request, recipe_id):
  ings = Ingredient.objects.filter(recipe__id__exact=recipe_id)
  cats = RecipeCategory.objects.filter(recipe__id__exact=recipe_id)
  r = get_object_or_404(Recipe, pk=recipe_id)
  return render_to_response('details.html', {'recipe' : r,
                                             'inglist' : ings,
                                             "catlist" : cats} )

