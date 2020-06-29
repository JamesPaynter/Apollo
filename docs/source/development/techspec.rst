.. James Paynter, 2020.
.. _techspec:

Apollo Technical Specification
==============================

Quasar microlensing software suite.








Modules
-------


Quasar module
^^^^^^^^^^^^^


-	  QSO = Quasar(\*\*kwargs)
 	    - Mass
 	    - inclination angle
 	    - type (solid disk, etc.)
 	    - Luminosity / eddington
-	  QSO.plot(show or savefig)
 	    - show
 	    - savefig
-	  QSO.return_disk()


Questions
"""""""""

1.  How does matplotlib do image scaling?
      a. Do I need to do manual image rescaling myself?
      b.


Magmap module
^^^^^^^^^^^^^

-	  Magmap = MagnificationMap(\*\*kwargs)
-	  Magmap.plot(show or savefig)
-	  Magmap.return_strip(\*args)


Convolve module
^^^^^^^^^^^^^^^


Telescope module
^^^^^^^^^^^^^^^^






Animations
----------
