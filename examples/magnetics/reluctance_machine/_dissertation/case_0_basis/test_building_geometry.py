from src.executor import Executor
import machine_model as model

variables = model.VariableParameters(output_folder_name='test',
                                      output_file_name='test',
                                     output_file_counter=0,
                                     current_density=0,
                                     initial_current_angle=0,
                                     current_angle=0,
                                     rotor_position=0,
                                     X1_cut_off_barrier_opening_angle=20,
                                     X2_cut_off_barrier_curve_angle=130,
                                     X3_cut_off_barrier_internal_barrier_distance=1,
                                     X4_rib_width_upper=0.1,
                                     X5_internal_barrier_height_upper=4,
                                     X6_internal_barrier_lower_barrier_distance=2,
                                     X7_rib_width_lower=0.1,
                                     X8_internal_barrier_height_lower=4,
                                     X9_magnet_pocket_width=15,
                                     X10_magnet_pocket_height=2,
                                     X11_magnet_pocket_shift=3,
                                     X12_distance_magnet_pocket_internal_barrier=0.5,
                                     X13_distance_internal_barriers=0,
                                     X14_magnet_width=0,
                                     X15_magnet_height=0,
                                     X16_magnet_shift=0
                                     )

model.model_creation(variables)

femm = Executor()

# Execute the .lua file.
femm.run(variables.output_file_path + '.lua')
