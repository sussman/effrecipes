
# EffRecipes main product
# Written for the Zope API
# (C) 2004 Ben Collins-Sussman under the GNU GPL.

import RecipeCatalog


# This registers the whole RecipeCatalog class with Zope as a "product",
# so that a RecipeCatalog can be instantiated directly via Zope's web
# management interface.

def initialize(context):

  context.registerClass(
    RecipeCatalog.RecipeCatalog,
    permission="Add Recipe Catalog",
    constructors=(RecipeCatalog.manage_addRecipeCatalogForm,
                  RecipeCatalog.manage_addRecipeCatalog)
    )
