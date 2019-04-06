#!/usr/bin/python
import sys, os
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sed_data import GrainInfo


class MPM:
    # This class computes solid transport according to Meyer-Peter and Mueller formula.
    def __init__(self, input_dir):
        self.grains = GrainInfo(input_dir)
        self.grains()
        self.taux = np.nan
        self.taux_cr = 0.047
        self.g = 9.81
        self.s = 2.68
        self.warnings = []
        self.hMorph = np.nan
        print(' * loaded solid transport formulae from Meyer-Peter and Mueller (1948)')

    def check_validity(self, J, D, Q, h, Fr, k):
        warning_msg = ''
        if (J < 0.0004) or (J > 0.02):
            warning_msg = 'Warning: Slope out of validity range.'
            print(warning_msg + ' (Q = {0} m3/s, D = {1} m)'.format(Q, D))
        if (D < 0.0004) or (D > 0.03):
            warning_msg = 'Warning: Grain size out of validity range.'
            print(warning_msg + ' (Q = {0} m3/s, D = {1} m)'.format(Q, D))
        if (Q / h < 0.002) or (Q / h > 2):
            warning_msg = 'Warning: Discharge out of validity range.'
            print(warning_msg + ' (Q = {0} m3/s, D = {1} m)'.format(Q, D))
        if (self.s < 0.25) or (self.s > 3.2):
            warning_msg = 'Warning: Relative grain density (s) out of validity range.'
            print(warning_msg + ' (Q = {0} m3/s, D = {1} m)'.format(Q, D))
        if (h < 0.01) or (h > 1.2):
            warning_msg = 'Warning: Flow depth out of validity range.'
            print(warning_msg + ' (Q = {0} m3/s, D = {1} m)'.format(Q, D))
        return warning_msg


    def compute_MPM(self, Di, Rh, J):
        _taux = self.compute_taux(J, Rh, Di)
        if 0.85*_taux > self.taux_cr:
            __qx = 8*(0.85*_taux-self.taux_cr)**(3/2)
        else:
            __qx = 0
        return(__qx)

    def compute_hmorph(self, J, iD, kst):
        # computation of the Hydraulic Radius for incipient grain motion based on Dm
        _hMorph = self.taux_cr / 0.85 * self.grains.Dm[iD] * (self.s - 1) / J
        return _hMorph

    def compute_taux(self, J, Rh, D):
        _taux = J * Rh / ((self.s - 1) * D)
        return _taux

    def __call__(self, J, Q, RhL, RhC, RhR, wL, wC, wR, uL, uC, uR, Fr, k):
        print(' * calculating ...')
        _Qb = np.nan * np.ones((self.grains.classes + 1, 1))
        _pD = 0
        for ik in range(0, self.grains.classes + 1):
            if not (np.isnan(self.grains.data[ik, k])):
                _fac = self.grains.percentages[ik+1] - _pD
                _QbL = self.compute_MPM(self.grains.data[ik, k], RhL, J) * wL / 2
                _QbC = self.compute_MPM(self.grains.data[ik, k], RhC, J) * wC
                _QbR = self.compute_MPM(self.grains.data[ik, k], RhR, J) * wR / 2
                #          Qb      kg/s
                _Qb[ik] = (_QbL + _QbC + _QbR) * np.sqrt(self.g * (self.s - 1) * self.grains.data[ik, k] ** 3) * self.s * _fac * 1000
                _pD = self.grains.percentages[ik + 1]
            else:
                _Qb[ik] = 0
        return np.nansum(_Qb)


