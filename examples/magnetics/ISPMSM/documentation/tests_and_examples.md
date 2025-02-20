# Tests for the Electric Machine Torque Calculations

## Some tests that are also intended as an example which helps to represent the physics behind the simulations

This documentation serves a sum of examples which were calculated during the tests of the codebase. There are some
tricks and tips regarding the code and the physics and also the limitations are highlighted. The documentation is not
intended to cover all the physics behind the simulations. It assumes a basic knowledge in electric engineering. For a 
complete coverage refer to the Design of **Rotating Electrical Machines, Juha Pyrhönen, Tapani Jokinen, Valéria Hrabovcová, 
DOI:10.1002/9781118701591** or for hungarian speaking fellows **Villamos Gépek** series from **József Liska**.

* Distributed winding, 1 layer, 12 slots and 4 poles
* Distributed winding, 2 layers, 1 shortening, 12 slots and 4 poles
* Concentrated winding, 12 slots and 8 poles

## Distributed winding, 1 layer, 12 slots and 4 poles

Winding scheme: **A|b|C|a|B|c|A|b|C|a|B|c|** (https://www.bavaria-direct.co.za/scheme/calculator/)

        start up run_selector.py

![img_1.png](img_1.png)

### Selecting cogging torque calculation (COGGING).

Cogging torque is an unwanted torque ripple that occurs in electric machines due to the interaction between the
permanent magnets of the rotor and the stator teeth. Cogging torque results from variations in magnetic reluctance as 
the rotor moves relative to the stator. This effect is particularly noticeable in permanent magnet synchronous machines
(PMSMs), leading to vibration, noise, and reduced smoothness in motion.

* Rotate the rotor in small steps (e.g., 1° or less) over an electrical period. For each step, compute the 
electromagnetic torque using FEM.

An electrical period for this slot/magnet pole combination will have 12 cogging steps per turn due to the Least Common
Multiple _LCM(12,4)=**12**_. It means that 12 period is present over one rotation, so over 360 mechanical degrees. 
To decrease the computational burden _360/12=**30**_ degrees is enough to calculate one period of the cogging torque.

![img.png](img.png)

After selecting the _cogging_ option the parameter list jumps up shown above. First of all, every parameter is limited
to a given input type. Those parameters are always checked for valid input and the program will not start until all
differences are solved. Please keep that in mind!

        int/float:          int (integer) means discrete whole-number values, and float (floating-point) means
                            continuous decimal values, allowing for higher precision

        int/float/pos:      int (integer) means discrete whole-number values, and float (floating-point) means
                            continuous decimal values, allowing for higher precision but only positive numbers higher
                            than zero (>0)

        int/pos:            int (integer) means discrete whole-number values, but only positive numbers higher than
                            zero (>0)

        str:                str (string) is a sequence of characters used to represent text

1) **initial_rotor_position [mechanical degrees]:** set the initial rotor position in mechanical degrees, which helps to
position the rotor where the torque of the first calculation is zero. It helps to find the starting point of a period.
The starting point depends on the number of poles, the winding scheme, the shortening and the rotor geometry. It is not
a neccessary step but helps to interpret an plot the results. The easiest way to determine the starting point run the
the cogging torque calculation and correct for the second run.


2) **rotor_diameter [millimeters]:** set the rotor diameter (shown in the image below). Be aware that the rotor diameter
should be larger than the shaft diameter. Plus, keep in mind that there should be enough space for the magnets to
accommodate. Please input a positive number.


3) **shaft_diameter [millimeters]:** set the shaft diameter (shown in the image below). Be aware that the shaft diameter
should be lower than the rotor diameter. Plus, keep in mind that there should be enough space for the magnets to
accommodate. Please input a positive number. Please input a positive number.


4) **magnet_width [degrees]:** set the width of the magnets (shown in the image below). As an ISPMSM the magnets are
inset to the circumference of the rotor and bent to the circle arc of the rotor, so it is more convenient to define the
width in degrees. Be aware that the magnet width cannot be larger than the width of a pole which is calculated from the
number of poles _360/4=**90**_. Please input a positive number.


5) **magnet_height [millimeters]:** set the height of the magnets (shown in the image below). Keep in mind that the 
magnet cannot be larger than the half of difference of the rotor diameter and the shaft diameter. Please input a 
positive number.


6) **pole_pairs [-]**: set the number of pole pairs. Be aware that it is the half of the number of poles. This
convention is a tribute to the Hungarian professors who have contributed a lot to the development of Hungarian 
electrical engineering of electric machines. Be aware that some slot and pole combination is not viable, so check every
time with https://www.bavaria-direct.co.za/scheme/calculator/.


7) **stack_length [millimeters]:** set 



