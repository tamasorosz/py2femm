import femm
import numpy as np

coords = [
    (17.668365, 2.7460545),
    (14.4351745, 10.551667),
    (10.5516665, 14.4351745),
    (2.7460545, 17.6683645),
    (7.0444815, 19.893003),
    (19.047678, 9.085276),
    (5, 5)
]

# values = [i*0.175781 / 2 for i in range(8192)][0:257]

values = np.linspace(-15,0,256)

femm.openfemm()
femm.opendocument("steel.fem")

with open("2D_FEMM_Steel_18mm_full.csv", "a") as file_out:
    for i in values:
        femm.mi_modifyboundprop('pbca', 10, i)
        femm.mi_analyze(1)
        femm.mi_loadsolution()

        for x, y in coords:
            femm.mo_selectblock(x, y)

        wTorque_0 = femm.mo_blockintegral(22) * 4
        femm.mo_clearblock()
        file_out.write(f"{wTorque_0}\n")

femm.closefemm()
