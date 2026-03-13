import math

import machine_model_synrm

variables = machine_model_synrm.VariableParameters(fold='ang',
                                                   out='ang',
                                                   counter=0,
                                                   JAp=10,
                                                   JAn=-10,
                                                   JBp=-5,
                                                   JBn=5,
                                                   JCp=-5,
                                                   JCn=5,

                                                   ang_co=24.3,
                                                   deg_co=91.5,
                                                   bd=1.0,
                                                   bw=0.5,
                                                   bh=2.4,
                                                   bg=1.5,

                                                   ia=0
                                                   )
machine_model_synrm.run_model(variables)
