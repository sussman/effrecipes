# (C) 2003 Ben Collins-Sussman under the GNU General Public License.
# See the file COPYING for details.

# Initialization of recipe MySQL tables.  This code assumes that an
# empty 'effrecipes' database has already been created.

USE effrecipes;

# Main table of recipes.
CREATE TABLE recipes
  (       
    RecipeId       INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Name           VARCHAR(255),
    Rating         INT,
    Instructions   TEXT,
    Commentary     TEXT,
    ServingHistory TEXT,
    Attribution    TEXT
  );


# Categories:  breads, cakes, salads, etc.
CREATE TABLE categories
  (
    CatId       INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Name        VARCHAR(100)
  );


# Category lists:  each recipe might belong to N categories.
# A single recipe has *multiple* rows in this table.
CREATE TABLE category_lists
  (
    RecipeId    INT,       # non-unique
    CatId       INT
  );


# Units:  teaspoon, tablespoons, cups, etc.
CREATE TABLE units
  (
    UnitId      INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Name        VARCHAR(100)
  );


# Every kind of food:  bananas, flour, eggs, etc.
CREATE TABLE ingredients
  (
    IngId       INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Name        VARCHAR(255)
  );

# Each recipe has *multiple* rows in this table, thus specifying its
# ingredient list.
CREATE TABLE ingredient_quantities
  (
    RecipeId    INT,  # non-unique
    Amount      REAL, # 3
    UnitId      INT,  # cups
    IngId       INT,  # spinach
    Verb        TEXT  # "chopped"
  );

# A typical user database, for users of the system.
CREATE TABLE users
  (
    UserId      INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Username    VARCHAR(30),
    Password    VARCHAR(15),
    Realname    VARCHAR(50),
    Email       VARCHAR(80)
  );

# Multiple entries per user, allowing them to list likes/dislikes/allergies.
CREATE TABLE userprefs
  (
    UserId      INT,         # non-unique
    IngId       INT,
    Kind        ENUM('like', 'dislike', 'allergy')
  );

# Mulitple entries per user, allowing them to rate a recipe.
CREATE TABLE votes
  (
    RecipeId    INT,         # UNIQUE key #1
    UserId      INT,         # UNIQUE key #2
    Vote        INT
  );

# Sanity check -- print out the list of tables.
SHOW TABLES;
