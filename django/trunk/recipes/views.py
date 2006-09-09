from django.http import HttpResponse

# From the tutorial: every URL callback must either return an
# HttpResponse object containing page content, or must raise an http
# exception.


# Front page of site
def index(request):
    return HttpResponse("Hello, world. You're at the recipe index.")


# Read-only view of a single recipe
def detail(request, recipe_id):
    return HttpResponse("You're looking at recipe %s." % recipe_id)

