# Run this script as the mysql 'root' user!

# Create an empty 'effrecipes' database
CREATE DATABASE effrecipes;

# Create an 'effuser' mysql user with permission to change this database.
# User's password is also 'effuser'.

USE mysql;

GRANT ALL PRIVILEGES ON effrecipes
      TO effuser@localhost IDENTIFIED BY 'effuser';

