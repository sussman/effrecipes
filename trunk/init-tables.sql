CREATE DATABASE effrecipes;
USE effrecipes;

# Main table of recipes.
CREATE TABLE recipes
  (       
    RecipeId       INT,
    Name           VARCHAR(255),
    Categories     INT,    # should be a list of CatIds, but how???          
    Rating         INT,
    Instructions   TEXT,
    Commentary     TEXT,
    ServingHistory TEXT,
    Attribution    TEXT
  );


# Categories:  breads, cakes, salads, etc.
CREATE TABLE categories
  (
    CatId       INT,
    Name        VARCHAR(100)
  );

# Units:  teaspoon, tablespoons, cups, etc.
CREATE TABLE units
  (
    UnitId      INT,
    Name        VARCHAR(100)
  );

# Every kind of food:  bananas, flour, eggs, etc.
CREATE TABLE ingredients
  (
    IngId       INT,
    Name        VARCHAR(255)
  );

# Each recipe has *multiple* rows in this table, thus specifying its
# ingredient list.
CREATE TABLE ingredient_lists
  (
    RecipeId    INT,
    Amount      REAL,
    UnitId      INT,
    IngId       INT
  );

# A typical user database, for users of the system.
CREATE TABLE users
  (
    UserId      INT,
    Username    VARCHAR(30),
    Password    VARCHAR(15),
    Realname    VARCHAR(50),
    Email       VARCHAR(80)
  );

# Multiple entries per user, allowing them to list likes/dislikes/allergies.
CREATE TABLE userprefs
  (
    UserId      INT,
    IngId       INT,
    Kind        ENUM('like', 'dislike', 'allergy')
  );

# Mulitple entries per user, allowing them to rate a recipe.
CREATE TABLE votes
  (
    RecipeId    INT,
    UserId      INT,
    Vote        INT
  );
