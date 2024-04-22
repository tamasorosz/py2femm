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
                                                   ang_co=10,
                                                   deg_co=90,
                                                   bd=2,
                                                   bw=1,
                                                   bh=2,
                                                   bg=1
                                                   )

machine_model_synrm.run_model(variables)
