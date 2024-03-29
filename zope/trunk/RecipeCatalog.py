
# EffRecipes:  a top-level container class to hold recipes.
# Written for the Zope API.
# (C) 2004 Ben Collins-Sussman under the GNU GPL.

from OFS.SimpleItem import SimpleItem
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
#from Globals import HTMLFile


# Global constructors for the module, referenced by __init__.py.
# These methods allow the ZMI to "add" a new RecipeCatalog object.

manage_addRecipeCatalogForm = PageTemplateFile(
  "templates/addRecipeCatalogForm.html",
  globals())


def manage_addRecipeCatalog(self, id, title, REQUEST):
  "Add a new RecipeCatalog object to a folder."

  # create a new RecipeCatalog
  newRecipeCatalog = RecipeCatalog(id, title)

  # this is the parent folder's method;  add the new object to parent.
  self._setObject(id, newRecipeCatalog)

  # then have the object display itself.
  return self.manage_main(self, REQUEST)




# The actual RecipeCatalog class.

# By subclassing OFS.SimpleItem, we automatically inherit all sorts of
# critical things, such as object persistence (!), acquisition
# behaviors, and the ability to interact with the Zope Management
# Interface (ZMI).

class RecipeCatalog(SimpleItem):
  "The RecipeCatalog object."

  # The ZMI categorizes all objects, so you can filter them
  meta_type = "RecipeCatalog"

  # An object that represents the main management view.  This is
  # effectively the "display" function of this class, although it
  # displays the object as a set of editable fields with a submit-button.
  manage_main = PageTemplateFile("templates/mainRecipeCatalog.html", globals())

  # Create custom tabs in the ZMI to execute custom methods.
  # (We're overriding an inherited global from SimpleItem; it's a
  # tuple of two-item dictionaries, each representing a tab.)  
  manage_options=({'label':'Edit',
                   'action':'manage_main'},
                  {'label':'View',
                   'action':'index_html'},
                  )
  
  # constructor
  def __init__(self, id, title):
    self.id = id
    self.title = title

  # main write accessor
  def editRecipeCatalog(self, title, REQUEST):
    "Change the properties of a RecipeCatalog."

    self.title = title
    # After changing the object, have the object redisplay itself.
    #return self.manage_main(self, REQUEST)

  # a read accessor
  def getTitle(self):
    "Return the title of a RecipeCatalog."
    return self.title


  # Web Presentation Methods

  # a method name Zope expects:
  index_html = PageTemplateFile("templates/indexRecipeCatalog.html", globals())
