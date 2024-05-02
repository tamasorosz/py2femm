import math

import machine_model_synrm

a = 15
b = 4
c = 1
g = 1.5

variables = machine_model_synrm.VariableParameters(fold='ang',
                                                   out='ang',
                                                   counter=0,
                                                   JAp=10,
                                                   JAn=-10,
                                                   JBp=-5,
                                                   JBn=5,
                                                   JCp=-5,
                                                   JCn=5,

                                                   ang_co=a,
                                                   deg_co=150,
                                                   bd=b,
                                                   bw=0.5,
                                                   bh=c,
                                                   bg=g,

                                                   ia=0
                                                   )
machine_model_synrm.run_model(variables)
print("C1 = " + str(math.tan(math.radians(a/2)) * (22 - g)))
print("C2 = " + str(b))
print("C3 = " + str(c))
print(str(math.tan(math.radians(a/2)) * (22 - g) + b + c))