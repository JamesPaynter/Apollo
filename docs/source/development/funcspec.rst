.. James Paynter, 2020.
.. _funcspec:

Apollo Functionality Specification
==================================

Quasar microlensing software suite.


Overview
--------

Apollo is a software suite for
Downloading magnification maps from the internet
Magnification maps take several days to process and download off the GERLPUMPH server.
A download request is then emailed to the user.
This could be automated but probably not worth the time
1.	Pre-processing magnification maps
2.	Simulating (simple) quasar accretion disks
3.	Formatting quasar simulations for image convolution
4.	Convolving image
a.	Including functionality for animations of this process
5.	Fitting light-curves with theoretical microlensing caustic curve equations
6.	Triggering mechanism(s) for targets of opportunity which exceed a given threshold
7. Animate functionality should be inbuilt from beginning (eg. Light-curve from caustic crossing over a few Einstein radii)
8.	All this should be done both from scripts (and possibly CLI), and from a GUI (point and click)



Users
-----

Me
^^^

The core user of the apollo-microlens suite.
Not sure of the complete functionality at this point so I am writing this func spec to iron out the kinks.


Masters' students
^^^^^^^^^^^^^^^^^

Students in the same research group or further afield may want to use this code.
They may not have strong coding skills and therefore simple user interface will benefit them.
A graphical user interface will greatly benefit them.
Clear documentation will be the key to their success.


Research supervisors
^^^^^^^^^^^^^^^^^^^^

They do not want to hear not hide nor hair of the source code.
They can be impressed with good science, pretty plots, and flashy animations.


Paper Referees
^^^^^^^^^^^^^^

They probably care not for the inner workings of your software, but may be placated with working tests that prove that it works as advertised on the box.


Software Referees
^^^^^^^^^^^^^^^^^

Will want to see unit tests aplenty, with a dash of integration testing.
They will be on the lookout for clear and coherent APIs and documentation.
Will likely test that the software works on their computer.


Conclusions
^^^^^^^^^^^
-   Clear documentation
-   Extensive unit testing and integration testing
-   Pretty plots and flashy animations
-   Working GUI




Non-goals
---------

-   This project will not perform hydrodynamic simulations of accreting gas to simulate quasars.
    We will take an analytic approach to our quasars, with appropriate parameterisations pulled from the literature.
-   This software will not create its own magnification maps, except for extremely simply maps used for testing.




Flowchart
---------

TODO



Main GUI
--------

-	  Show full microlens map on the screen
-	  Click to place quasar
-	  Dotted square / circle indicates full region which will be involved in convolution
-	  Click to place quasar end point
-	  Select velocity (and other parameters if there are any?)
-	  Convolve quasar image with magnification map over path
-	  Create animation


Extra (low priority)
^^^^^^^^^^^^^^^^^^^^

-	  Web hosted GUI / library
 	    - Which is able to access / inherit most of the same code as the main GUI


Features
^^^^^^^^

-	  Drop down menu box for magnification map selection (shows map features
-	  Box for selection lensing parameters, (source and lens redshift)
-	  Click and drop quasars
-	  Drop down menu box to select quasar type (how light curve is produced)
 	    -	Quasars should scale with black hole mass
 	    - And potentially with Eddington luminosity
