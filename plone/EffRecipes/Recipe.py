
from Products.Archetypes.public import BaseSchema, Schema

from Products.Archetypes.public import StringField, TextField
from Products.Archetypes.public import SelectionWidget, TextAreaWidget
from Products.Archetypes.public import RichWidget, VisualWidget
from Products.Archetypes.public import IntegerField, IntegerWidget
from Products.Archetypes.public import ImageField, ImageWidget

from Products.Archetypes.public import BaseContent, registerType
from Products.Archetypes.Marshall import PrimaryFieldMarshaller
from Products.CMFCore import CMFCorePermissions
from config import PROJECTNAME

schema = BaseSchema +  Schema((
  
  IntegerField("servings",
               widget=IntegerWidget(label="Servings",
                                    description="How many servings does this recipe make?"),
               ),

  ImageField("picture",
             widget=ImageWidget(label="Picture",
                                description="If you have a photo available, upload it here."),
             display_threshold=100000,
             ),

  TextField('ingredients',
            searchable=1,
            required=1,
            rows=8,
            format=1,
            widget=TextAreaWidget(label="Ingredients",
                                  description="This is very tricky, see docs."),
            ),

  TextField('instructions',
            searchable=1,
            required=1,
            primary=1,   # this field will be returned by DAV and FTP
            rows=10,
            widget=TextAreaWidget(label="Instructions",
                                  description="Describe how to prepare the food."),
            ),

  TextField('servinghistory',
            searchable=1,
            rows=5,
            widget=TextAreaWidget(label="Serving History",
                                  description="When was this dish served?"),
            ),

  StringField('attribution',
              searchable=1,
              rows=3,
              widget=TextAreaWidget(label="Attribution",
                                    description="Where did this recipe come from?"),
              ),
  ),
                              
                              marshall=PrimaryFieldMarshaller(),
                              )




class Recipe(BaseContent):
  """A basic cookbook recipe type.
  """
  
  # Use our schema to generate the new type.
  schema = schema
    
  def allowDiscussion(self):
    "Enable discussion on all recipe documents by default."
    return True


  def validate_ingredients(self, value):
    """Make sure ingredients field is properly formatted.
    Return None for no error, or string describing error.
    """
    return None 


    
  ### make a nicer looking CSS display of recipe?

#    actions = ({
#        'id': 'view',
#        'name': 'View',
#        'action': 'string:${object_url}/recipe_view',
#        'permissions': (CMFCorePermissions.View,)
#        },)

registerType(Recipe, PROJECTNAME)
