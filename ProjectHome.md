This is Ben Collins-Sussman's attempt to write a web-based recipe database for his wife.  The first three attempts failed, though they're in the svn repository for posterity:

**Attempt #1: Code MySQL tables by hand, code python object persistence layer by hand, code CGI UI by hand.  Ugly, slow, and yucky.**

**Attempt #2: Use Zope.  Way too hard.  Like hitting a fly with a buick.**

**Attempt #3:  Use Plone.  Define objects via 'archetype' schema, as if everything were a document in the content management system.  Close, but still not quite a good fit.  Could never get it to work right.**

The fourth attempt seems to have worked.  Django is 'just right'.  Fast, simple, and exactly what I was looking for.