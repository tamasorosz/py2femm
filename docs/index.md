---
permalink: /index/
---

# Manual for py2femm

This library aims to provide a cross-platform, Python-based interface for [FEMM](https://www.femm.info/wiki/HomePage), a
popular finite element method-based solver. It provides a GUI to solve two-dimensional electromagnetic and thermal
problems.
It has an officially supported [python interface (pyFEMM)](https://www.femm.info/wiki/pyFEMM). However, it works on the
Windows operating system only.  
It is possible to run FEMM under Linux operating systems with [Wine](https://www.winehq.org/). However, it does not
support the ActiveX interface, which was used by the original solution.

This project provides a file-based interface for FEMM, which can be used with Wine and under Linux operating systems.
This interface generates a lua file, which the original interpreter of FEMM can use. However, this interface differs
from the original command set in the following points:

The geometry description is separated from the fields; therefore, if we describe the geometry for a 2D magnetic model,
we can use the same description of the part to create the thermal model.

Some new commands are introduced, which execute the combination of some straightforward commands.


docs/geometry_generation.md