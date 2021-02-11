from enum import Enum


class SkinMaterialParameters:
    def __init__(self, rho: float, Ef: float, sigma_af: float, Cost: float):
        self.rho = rho
        self.Ef = Ef  # Longitudinal Elastic Modulus
        self.sigma_af = sigma_af  # Permissible Stress
        self.Cost = Cost  # euro/kg


class CoreMaterialParameters:
    def __init__(self, rho: float, Ec: float, Gc: float, tau_ac: float, Cost: float):
        self.rho = rho
        self.Ec = Ec  # Longitudinal Elastic Modulus
        self.Gc = Gc  # Transversal Elastic Modulus
        self.tau_ac = tau_ac  # Permissible Shear Stress
        self.Cost = Cost


class BeamModel:
    def __init__(self, L: float, b: float, tf: float, tc: float, skinMat: SkinMaterialParameters,
                 coreMat: CoreMaterialParameters):
        self.L = L  # Length
        self.b = b  # Width
        self.tf = tf  # Skin height
        self.tc = tc  # Core height
        self.SkinMat = skinMat  # Material for the skin
        self.CoreMat = coreMat  # Material for the core


class BeamSimulation:
    def __init__(self, m: float, a: float, km: float, model: BeamModel, sf: float):
        self.m = m
        self.a = a
        self.km = km
        self.model = model
        self.sf = sf


class SkinMaterials(Enum):
    Steel = 0
    Aluminium = 1
    GFRP = 2
    CFRP = 3


class CoreMaterials(Enum):
    DivinycellH60 = 0
    DivinycellH100 = 1
    DivinycellH130 = 2
    DivinycellH200 = 3


skin_materials = {
    SkinMaterials.Steel: SkinMaterialParameters(7800, 205000 * 1e6, 300 * 1e6, 0.4),
    SkinMaterials.Aluminium: SkinMaterialParameters(2700, 70000 * 1e6, 200 * 1e6, 0.7),
    SkinMaterials.GFRP: SkinMaterialParameters(1600, 20000 * 1e6, 400 * 1e6, 4),
    SkinMaterials.CFRP: SkinMaterialParameters(1500, 70000 * 1e6, 1000 * 1e6, 80)
}
core_materials = {
    CoreMaterials.DivinycellH60: CoreMaterialParameters(60, 55 * 1e6, 22 * 1e6, 0.6 * 1e6, 6),
    CoreMaterials.DivinycellH100: CoreMaterialParameters(100, 95 * 1e6, 38 * 1e6, 1.2 * 1e6, 10),
    CoreMaterials.DivinycellH130: CoreMaterialParameters(130, 125 * 1e6, 47 * 1e6, 1.6 * 1e6, 13),
    CoreMaterials.DivinycellH200: CoreMaterialParameters(200, 195 * 1e6, 75 * 1e6, 3.0 * 1e6, 20),
}


# noinspection DuplicatedCode,PyAttributeOutsideInit
class Result:
    def __init__(self, simulation):
        self.simulation = simulation

    def Solve(self):
        simulation = self.simulation

        # Gather all the input variables to make the formulas look nice
        m = simulation.m
        a = simulation.a
        sf = simulation.sf
        km = simulation.km
        sigma_af = simulation.model.SkinMat.sigma_af
        tau_ac = simulation.model.CoreMat.tau_ac
        L = simulation.model.L
        b = simulation.model.b
        tf = simulation.model.tf
        tc = simulation.model.tc
        Ef = simulation.model.SkinMat.Ef
        Ec = simulation.model.CoreMat.Ec
        Gc = simulation.model.CoreMat.Gc
        rho_f = simulation.model.SkinMat.rho
        rho_c = simulation.model.CoreMat.rho
        cost_f = simulation.model.SkinMat.Cost
        cost_c = simulation.model.CoreMat.Cost

        # Now solve all the equations described above and store in data members the values we're interested in
        # Actual Load (Force here)
        P = m * a

        # Moment over the length of the beam
        M = P * L

        # Imposed displacement based on the rigidity
        Wm = P / km

        # Maximum stress
        sigma_af = sigma_af / sf
        tau_ac = tau_ac / sf

        # Volumes
        Vf = 2 * tf * L * b
        Vc = tc * L * b

        # Total cost
        Cost = Vf * rho_f * cost_f + Vc * rho_c * cost_c

        # Distance between middle of shell to middle of shell
        d = tf + tc

        D = (Ef * tf * d ** 2 / 2) * b
        S = (1 / tc) * Gc * d ** 2 * b
        W = (P * L ** 3) / (3 * D) + (P * L) / S

        # Actual shell stress
        sigma_f = M / D * Ef * d / 2

        # Actual core sheer stress
        tau_c = (P / D) * (Ec / 2 * ((tc ** 2) / 2) + Ef / 2 * (tf * tc + tf ** 2))

        # Total Mass
        Mt = Vf * rho_f + Vc * rho_c

        # Store the values we're interested in
        self.W = W
        self.Wm = Wm

        self.sigma_af = sigma_af
        self.sigma_f = sigma_f

        self.tau_ac = tau_ac
        self.tau_c = tau_c

        self.Cost = Cost
        self.Mt = Mt


class SimulationResult:

    def __init__(self, skin_mat, core_mat, L, tf, tc):
        self.tc = tc
        self.tf = tf
        self.L = L
        self.core_mat = core_mat
        self.skin_mat = skin_mat
