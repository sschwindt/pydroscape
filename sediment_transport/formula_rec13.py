#!/usr/bin/python
import sys, os
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sed_data import GrainInfo


class Rec13:
    # This class computes solid transport according to Alain Recking (2013) formula.
    def __init__(self, input_dir):
        self.grains = GrainInfo(input_dir)
        self.grains()
        self.taux = np.nan
        self.taux_cr = 0.047
        self.g = 9.81
        self.s = 2.68
        self.warnings = []
        self.hMorph = np.nan
        print(' * loaded solid transport formulae from Recking (2013)')

    def check_validity(self, *args, **kwargs):
        return ''

    def compute_rec13(self, J, Rh, k):
        if self.grains.D50[k] >= 0.002:
            # i.e. if gravel mixture
            tauXm = 12.53 * (1.32 * J + 0.037) ** 1.6 * (self.grains.D84[k] / self.grains.D50[k]) ** (4.4 * np.sqrt(J) - 0.93 * 1.6)
            print('Recking: Applied for gravel.')
        else:
            # i.e. for sand mixture
            tauXm = 0.045
            print('Recking: Applied for sand.')

        tauX84 = J * Rh / ((self.s - 1) * self.grains.D84[k])

#         --------------------- REC10 ---------------
#         tauXc84 = (1.32*J+0.037)*(self.grains.D84[k]/self.grains.D50[k])**(-0.93)
#         if tauXm < tauX84:  <
#             return 0.0005*(self.grains.D84[k]/self.grains.D50[k])**(-18*np.sqrt(J)) * (tauX84/tauXc84)**6.5
#         else:
#             return 14*tauX84**(5/2)

        return 14 * tauX84 ** (5 / 2) / (1 + (tauXm / tauX84) ** 4)

    def compute_hmorph(self, J, iD, kst):
        # computation of the Hydraulic depth for incipient grain motion based on Dm
        if iD == 0:
            print('Recking formula always implies a little sediment transport --> Qini = 0 m3/s.')
        _hMorph = np.nan
        return _hMorph

    def __call__(self, J, Q, RhL, RhC, RhR, wL, wC, wR, uL, uC, uR, Fr, k):
        _qxL = self.compute_rec13(J, RhL, k) * wL / 2
        _qxC = self.compute_rec13(J, RhC, k) * wC
        _qxR = self.compute_rec13(J, RhR, k) * wR / 2

        #  calculate sediment transport in                                       kg/s
        _Qb = (_qxL + _qxC + _qxR) * np.sqrt(self.g * (self.s - 1) * self.grains.D50[k] ** 3) * self.s * 1000
        return _Qb


