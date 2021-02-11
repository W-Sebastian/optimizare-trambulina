from computation import *
import sys


def material_to_enum(material: str):
    print(material)
    if material == "Steel":
        return SkinMaterials.Steel
    if material == "Aluminium":
        return SkinMaterials.Aluminium
    if material == "GFRP":
        return SkinMaterials.GFRP
    if material == "CFRP":
        return SkinMaterials.CFRP

    if material == "DivinycellH60":
        return CoreMaterials.DivinycellH60
    if material == "DivinycellH100":
        return CoreMaterials.DivinycellH100
    if material == "DivinycellH130":
        return CoreMaterials.DivinycellH130
    if material == "DivinycellH200":
        return CoreMaterials.DivinycellH200

    return None


if __name__ == "__main__":

    with open(sys.argv[1]) as in_file:
        tf = float(in_file.readline()) * 1e-3
        tc = float(in_file.readline()) * 1e-3
        L = float(in_file.readline())

        skin_mat_id = in_file.readline().strip()
        core_mat_id = in_file.readline().strip()

    b = 500 * 1e-3  # this is hardcoded and will remain at 500mm

    skinMat = skin_materials[material_to_enum(skin_mat_id)]
    coreMat = core_materials[material_to_enum(core_mat_id)]

    model = BeamModel(L, b, tf, tc, skinMat, coreMat)

    m = 150  # kg - this is fixed
    a = 9.80665  # m/s^2 - we would need to have higher accelerations to account for jumps
    km = 5000  # N/m - fixed
    sf = 5  # safety factor

    simulation = BeamSimulation(m, a, km, model, sf)

    res = Result(simulation)
    res.Solve()

    with open(r'out2.txt', 'a') as out_file2:
        out_file2.write('|')

    with open(r'out.txt', 'w') as out_file:
        out_file.write('{:.5f}\n'.format(res.W*1e3))
        out_file.write('{:.5f}\n'.format(res.Wm * 1e3))

        out_file.write('{:.5f}\n'.format(res.tau_c * 1e-6))
        out_file.write('{:.5f}\n'.format(res.tau_ac * 1e-6))

        out_file.write('{:.5f}\n'.format(res.sigma_f * 1e-6))
        out_file.write('{:.5f}\n'.format(res.sigma_af * 1e-6))

        out_file.write('{:.2f}\n'.format(res.Cost))
        out_file.write('{:.5f}\n'.format(res.Mt))

    sys.exit(0)
