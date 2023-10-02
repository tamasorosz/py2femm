# py2femm

An alternative library to run FEMM simulations under windows or linux environments, as well.

This python module realize a filelink interface, it generates the lua code and invokes the installed version of FEMM
directly as a subprocess.
This kind of communication work both under windows and linux platform using wine.

### New commands and further simplifications

* **define_block_label(x,y, material)**:
  simplifies the material definition process, you don't have to select and deselect the blocklabel from the lua code.
  This wrapper automatically puts the material with the following syntax:
  The material properties can be defined by the new material classes.
* set_boundary_definition
  Simplifies the step of the boundary definition, the user does not have to manually select/deselect the boundaries, it
  makes the changes in one step
* 