#!/usr/bin/env python2

# (C) 2003 Ben Collins-Sussman under the GNU General Public License.
# See the file COPYING for details.

# Edit a "Unit" record.

import MySQLdb, cgi, recipes

# enable debugging:  displays detailed exceptions in web browser.
import cgitb; cgitb.enable()

# -----------------------------------------------------------------

# Initialize database connection
conn = MySQLdb.connect(user='effuser', passwd='effuser', db='effrecipes')

# Initial generic HTML 'header' output
print "Content-type: text/html\n\n";
print "<html><head><title>Effrecipes - record saved</title>\n"
print "<h2>Saved record.</h2></head>\n\n"

# Use the CGI form values to create a new object and save it.
form = cgi.FieldStorage()

unit_object = recipes.Unit(int(form["unit_id"].value),
                           form["unit_name"].value)
unit_object.save(conn)

print "Record with Id ", form["unit_id"].value, "has been saved.<br/>\n"
print '<a href="frontpage.cgi">Go back to the front page</a>.\n'

# Cleanup and exit
print "</html>"
conn.close()

