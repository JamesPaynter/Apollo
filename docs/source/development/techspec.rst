.. James Paynter, 2020.
.. _techspec:

Apollo Technical Specification
==============================

Quasar microlensing software suite.






Have flush data command built into system to delete all non-protected data products / convolutions.
Need to build in protected list so the command knows what not to delete.

Is image scaling done at the Quasar / Magnificaiton map module, or at the convolve module?
(I think at the Convolve module makes more sense at this point)


Simulate Modules
----------------

The flow of the simulate module(s) will be the passing of an spectral cube through different layers / modules of the program.
The quasar class should create a 3D+1 model of a quasar (3 spatial dimensions + 1 spectral dimension).
This model is then flattened into 2D+1 (spatial + spectral).
The flattened 2D+1 spatial spectra is passed into the convolve module with a magnification map.

If you a priori know which bands you are going to observe the quasar in, then you can introduce the wavelength cutoffs at the beginning.

Notes
"""""

Will need to be able to account for 2D spatial models, and 2D+1 spatial and spectral models, where each pixel carries as full spectrum with it.
What are the units of the spectrum? (wavelength? Angstrom?)


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


Rotate Map
""""""""""

Need to save rotation angle metadata for convolutions.



Convolve module
^^^^^^^^^^^^^^^

Most of the meat will be in the convolve module.

Parameters needed

-	  Quasar (a 2D+1 array of flux/intensities)
-	  MagnificationMap (a 2D array of magnifications)
-	  Map orientation angle (rotate map in face on plane)
-	  Quasar redshift (source size)
-	  Image plane redshift (map size)
-	  Quasar centroid

For animations where are the timesteps calculated?
Does the map move or does the quasar move?
Boundary conditions? (or ban from boundary?)

Animation parameters
-	  Quasar end point

Telescope module
^^^^^^^^^^^^^^^^

Basically just bins in frequency space.
And applies noise filters, etc.




Animations
----------
