from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^effrecipes/', include('effrecipes.apps.foo.urls.foo')),

    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),

     (r'^recipes/$', 'effrecipes.recipes.views.index'),

     (r'^recipes/search/$', 'effrecipes.recipes.views.recipe_search'),

     (r'^recipes/category/(?P<category_id>.*)/$',
      'effrecipes.recipes.views.show_category'),

     (r'^recipes/(?P<recipe_id>\d+)/$', 'effrecipes.recipes.views.detail'),
)
