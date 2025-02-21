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
electromagnetic torque using FEM without any current.

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
a neccessary step but helps to interpret and plot the results. The easiest way to determine the starting point run the
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


7) **stack_length [millimeters]:** set the lenght of the electric machine's active parts. As the simulations run on a
cross-section model of a radial flux electric machine it assumes that the same flux is generated along the whole length
of the active parts. A rough estimation is that the torque increases linearly with the length of the active parts. 
Please input a positive number.


8) **winding_scheme [-]:** set the winding of the electric machine. As the type of the winding distinguishes the
two electric machines with the same geometry it is a complex field of study in engineering. Fortunately, there are some
websites that could help determine the possible winding schemes. One such website is https://www.emetor.com/windings/
which calculates the possible winding schemes and more for a given slot/poles combination. In this program the website 
https://www.bavaria-direct.co.za/scheme/calculator/ is utilised. Enter the number of slots (12) and number of poles (4)
and press calculate. The website gives you a string describing the winding scheme (A|b|C|a|B|c|A|b|C|a|B|c|).
Copy that into the **winding_scheme** slot. This program automatically recognise the structure and the layers. This
program accepts a winding structure given in the format of this website only.

![img_2.png](img_2.png)


9) **shortening [-]:** set the shortening of a 2 layer winding. It is not applicable in this case. Check the following
test cases.


10) **resolution [degrees]:** set the resolution of the cogging torque calculation between the starting rotor position and
the resulting rotor position. It is recommended to set it to a resolution of one degrees. A valid resolution is
calculated as _(**end_position_cogging** - **start_position_cogging** + 1)_. As previously mentioned you only need to
calculate one period of cogging torque if the machine is symmetrical which means if the **start_position_cogging** is
zero than one period ends at _360/12=**30**_ **end_position_cogging**. So the resolution should be **31**. If you want
a higher resolution for example 0.5 degrees thant the resolution should be **61**.


11) **start_position_cogging [mechanical degrees]:** set the starting rotor position of the calculation.
Should be lower than the **end_position_cogging**.


12) **end_position_cogging [mechanical degrees]:** set the ending rotor position of the calculation. 
As previously mentioned you only need to calculate one period of cogging torque if the machine is symmetrical
which means if the **start_position_cogging** is zero than one period ends at _360/12=**30**_ **end_position_cogging**.


13) **rounding [-]:** set the rounding of the resulting torque, using the np.round() function in Python, part of the 
NumPy library. It is used for rounding elements in an array to a specified number of decimal places.
It takes an array and an optional ‘decimals’. The function returns a new array with rounded values, without altering 
the original array. To get a distinguishable result, please use at least 1. For more precision use larger number.


14) **delete_after [bool]:** if True than the simulation files are deleted after the simulation ends, if false then the 
program stores the simulation files in the corresponding folder, in this case _cog_ folder.


15) **number_of_cores [-]:** set the number of cores used for the parallel calculations. Please do not use all the cores
of your machine as it may freeze.


16) **RUN SIMULATION:** the button starts the simulation. First it prints all the input variables to make it possible to
check manually. If the simulation end it prints the cogging torque, meaning the amplitude difference between the minimum
and maximum value in a period. It also prints all the calculated values as a list, plus plots it.

![img_3.png](img_3.png)

            The cogging torque is -4.798 Nm
            The list of torque values: [0.006, -0.335, -0.673, -1.011,
            -1.33, -1.63, -1.885, -2.097, -2.261, -2.36, -2.396, -2.333,
            -2.15, -1.768, -1.057, 0.001, 1.064, 1.782, 2.16, 2.343, 2.402,
            2.372, 2.266, 2.11, 1.896, 1.642, 1.338, 1.02, 0.682, 0.346, 0.002]

![img_4.png](img_4.png)

17) **BACK:** step back to the selector GUI.

### Selecting torque angle calculation (TORQUE ANGLE).

In a Permanent Magnet Synchronous Machines (PMSM), the torque is maximized when the rotor magnetic field is perpendicular
to the stator magnetic field. In a machine which has 2 poles so 1 pole pairs the electrical and mechanical degrees are
similar. In the case of higher pole pair numbers the the electrical angle is calculated as
_electrical_angle = mechanical_angle * pole_pair_number_. In the case of a perfectly symmetrical electric machine with
1 pole pairs the maximal torque is at the rotor position 90 degrees. With higher pole pair numbers like 2 it is 90/2=45
degrees and so on. It is really depends on the geometry of the rotor. This function aims to show how the rotor position
corresponding to the maximal torque varies in different cases.

* Rotate the rotor in small steps (e.g., 1° or less) over an electrical period. For each step, compute the
electromagnetic torque using FEM at a given current.

An electrical period for this slot/magnet pole combination will have two torque periods per turn due to the number of poles,
you should calculate at least half period the get the rotor position corresponding to the maximal torque. It is
recommended to calculate one period to understand working as a motor (positive torque) or as a generator (negative torque).

After selecting the _torque angle_ option the parameter list jumps up shown above. First of all, every parameter is limited
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

![img_5.png](img_5.png)

1) **current [A]:** set the peak value of the current used to excite the machine. The program automatically calculates
current value for each step in the rotation for each phase. 


2) **initial_current_angle [electrical degrees]:** set the current angle in electrical degrees, which helps to position
the stator magnetic filed to a position where the torque of the first calculation is zero. It helps to find the starting
point of a period. The starting point depends on the number of poles, the winding scheme, the shortening and the rotor
geometry. It is not a neccessary step but helps to interpret and plot the results. The easiest way to determine the 
starting point run the the torque angle calculation and correct for the second run. By default it should be zero.


3) **initial_rotor_position [mechanical degrees]:** set the initial rotor position in mechanical degrees, which helps to
position the rotor where the torque of the first calculation is zero. It helps to find the starting point of a period.
The starting point depends on the number of poles, the winding scheme, the shortening and the rotor geometry. It is not
a neccessary step but helps to interpret and plot the results. The easiest way to determine the starting point run the
the torque angle calculation and correct for the second run.


4) **rotor_diameter [millimeters]:** set the rotor diameter (shown in the image below). Be aware that the rotor diameter
should be larger than the shaft diameter. Plus, keep in mind that there should be enough space for the magnets to
accommodate. Please input a positive number.


5) **shaft_diameter [millimeters]:** set the shaft diameter (shown in the image below). Be aware that the shaft diameter
should be lower than the rotor diameter. Plus, keep in mind that there should be enough space for the magnets to
accommodate. Please input a positive number. Please input a positive number.


6) **magnet_width [degrees]:** set the width of the magnets (shown in the image below). As an ISPMSM the magnets are
inset to the circumference of the rotor and bent to the circle arc of the rotor, so it is more convenient to define the
width in degrees. Be aware that the magnet width cannot be larger than the width of a pole which is calculated from the
number of poles _360/4=**90**_. Please input a positive number.


7) **magnet_height [millimeters]:** set the height of the magnets (shown in the image below). Keep in mind that the 
magnet cannot be larger than the half of difference of the rotor diameter and the shaft diameter. Please input a 
positive number.


8) **pole_pairs [-]**: set the number of pole pairs. Be aware that it is the half of the number of poles. This
convention is a tribute to the Hungarian professors who have contributed a lot to the development of Hungarian 
electrical engineering of electric machines. Be aware that some slot and pole combination is not viable, so check every
time with https://www.bavaria-direct.co.za/scheme/calculator/.


9) **stack_length [millimeters]:** set the lenght of the electric machine's active parts. As the simulations run on a
cross-section model of a radial flux electric machine it assumes that the same flux is generated along the whole length
of the active parts. A rough estimation is that the torque increases linearly with the length of the active parts. 
Please input a positive number.


10) **winding_scheme [-]:** set the winding of the electric machine. As the type of the winding distinguishes the
two electric machines with the same geometry it is a complex field of study in engineering. Fortunately, there are some
websites that could help determine the possible winding schemes. One such website is https://www.emetor.com/windings/
which calculates the possible winding schemes and more for a given slot/poles combination. In this program the website 
https://www.bavaria-direct.co.za/scheme/calculator/ is utilised. Enter the number of slots (12) and number of poles (4)
and press calculate. The website gives you a string describing the winding scheme (A|b|C|a|B|c|A|b|C|a|B|c|).
Copy that into the **winding_scheme** slot. This program automatically recognise the structure and the layers. This
program accepts a winding structure given in the format of this website only.

![img_2.png](img_2.png)


11) **shortening [-]:** set the shortening of a 2 layer winding. It is not applicable in this case. Check the following
test cases.


12) **resolution [degrees]:** set the resolution of the torque angle calculation between the starting rotor position and
the resulting rotor position. It is recommended to set it to a resolution of one degrees. A valid resolution is
calculated as _(**end_position** - **start_position** + 1)_. As previously mentioned you only need to
calculate at least half period if the machine is symmetrical which means if the **start_position** is
zero than one period ends at _360/4=**90**_ **end_position**. So the resolution should be **91**. If you want
a higher resolution for example 0.5 degrees thant the resolution should be **181**.


13) **start_position [mechanical degrees]:** set the starting rotor position of the calculation.
Should be lower than the **end_position**.


14) **end_position [mechanical degrees]:** set the ending rotor position of the calculation. 
As previously mentioned you only need to calculate at least one period if the machine is symmetrical
which means if the **start_position** is zero than one period ends at _360/4=**90**_ **end_position**.


15) **rounding [-]:** set the rounding of the resulting torque, using the np.round() function in Python, part of the 
NumPy library. It is used for rounding elements in an array to a specified number of decimal places.
It takes an array and an optional ‘decimals’. The function returns a new array with rounded values, without altering 
the original array. To get a distinguishable result, please use at least 1. For more precision use larger number.


16) **delete_after [bool]:** if True than the simulation files are deleted after the simulation ends, if false then the 
program stores the simulation files in the corresponding folder, in this case _ang_ folder.


17) **number_of_cores [-]:** set the number of cores used for the parallel calculations. Please do not use all the cores
of your machine as it may freeze.


18) **RUN SIMULATION:** the button starts the simulation. First it prints all the input variables to make it possible to
check manually. If the simulation end it prints the rotor position corresponding to the maximal torque, meaning the 
amplitude difference between the minimum and maximum value in a period. It also prints all the calculated values as a
list, plus plots it.

![img_6.png](img_6.png)

    The rotor position where the torque is maximal: 40.0 deg
    The list of torque values: [-0.001, 2.125, 3.921,
    5.411, 6.674, 7.797, 8.799, 9.694, 10.519, 11.247,
    11.881, 12.45, 12.949, 13.361, 13.703, 13.986, 14.202,
    14.371, 14.478, 14.562, 14.599, 14.587, 14.551, 14.473,
    14.397, 14.329, 14.344, 14.485, 14.803, 15.404, 16.33, 17.34,
    18.157, 18.714, 19.104, 19.416, 19.649, 19.833, 19.977, 20.069,
    20.108, 20.095, 20.006, 19.841, 19.6, 19.29, 18.911, 18.485, 18.009,
    17.501, 16.953, 16.381, 15.788, 15.171, 14.547, 13.909, 13.293, 12.718,
    12.281, 12.122, 12.234, 12.42, 12.373, 12.062, 11.612, 11.096, 10.524,
    9.916, 9.277, 8.616, 7.944, 7.257, 6.583, 5.909, 5.253, 4.606, 3.98,
    3.372, 2.79, 2.239, 1.73, 1.262, 0.836, 0.448, 0.105, -0.192, -0.424,
    -0.567, -0.567, -0.352, 0.003, 0.358, 0.575, 0.574, 0.433, 0.2, -0.097,
    -0.444, -0.827, -1.248, -1.722, -2.233, -2.777, -3.365, -3.971, -4.602,
    -5.244, -5.899, -6.576, -7.253, -7.939, -8.611, -9.27, -9.91, -10.512,
    -11.092, -11.608, -12.058, -12.362, -12.412, -12.231, -12.115, -12.273,
    -12.712, -13.286, -13.903, -14.538, -15.165, -15.781, -16.375, -16.947,
    -17.491, -18.003, -18.484, -18.908, -19.282, -19.593, -19.834, -20.005,
    -20.083, -20.104, -20.062, -19.962, -19.826, -19.64, -19.408, -19.104,
    -18.703, -18.14, -17.323, -16.314, -15.385, -14.785, -14.474, -14.328,
    -14.317, -14.372, -14.456, -14.525, -14.567, -14.572, -14.543, -14.465,
    -14.347, -14.183, -13.964, -13.683, -13.343, -12.917, -12.431, -11.87,
    -11.225, -10.5, -9.69, -8.794, -7.785, -6.668, -5.407, -3.913, -2.094, -0.001]

![img_7.png](img_7.png)

19) **BACK:** step back to the selector GUI.

### Selecting average torque and torque ripple calculation (AVERAGE TORQUE).