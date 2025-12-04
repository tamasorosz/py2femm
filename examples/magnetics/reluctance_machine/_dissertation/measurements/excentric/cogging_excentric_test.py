import femm
import numpy as np

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return (rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(np.deg2rad(phi))
    y = rho * np.sin(np.deg2rad(phi))
    return (x, y)


# values = [i*0.175781 / 2 for i in range(8192)][0:257]

values = np.linspace(0,15,16)

femm.openfemm()
femm.opendocument("steel_full_base.fem")

for i in values:
    femm.mi_saveas(f'fem/cog_{i}.fem')

with open("2D_FEMM_Steel_18mm_full_base.csv", "a") as file_out:
    for i in values:
        femm.opendocument(f'fem/cog_{i}.fem')
        femm.mi_selectgroup(9)
        femm.mi_moverotate(0,0, i)
        femm.mi_analyze(1)
        femm.mi_loadsolution()

        coords_pol = [
            (4, 0),
            (7, 0),
            (21, 67.5 + i),
            (17, 80 + i),
            (17, 100 + i),
            (21, 115 + i),
            (17, 125 + i),
            (17, 145 + i),
            (21, 160 + i),
            (17, 170 + i),
            (17, -170 + i),
            (21, -160 + i),
            (17, -125 + i),
            (17, -145 + i),
            (21, -115 + i),
            (17, -80 + i),
            (17, -100 + i),
            (21, -67.5 + i),
            (17, -55 + i),
            (17, -35 + i),
            (21, -22.5 + i),
            (17, -10 + i),
            (17, 10 + i),
            (21, 22.5 + i),
            (17, 55 + i),
            (17, 35 + i)
        ]

        coords_cart = [pol2cart(j[0], j[1]) for j in coords_pol]

        for x, y in coords_cart:
            femm.mo_selectblock(x, y)

        wTorque_0 = femm.mo_blockintegral(22) * 4
        femm.mo_clearblock()
        file_out.write(f"{wTorque_0}\n")