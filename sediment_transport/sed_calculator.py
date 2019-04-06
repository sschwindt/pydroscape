#!/usr/bin/python
import sys, os
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from sed_data import HEC1D, GrainInfo
    from formula_aw import AW
    from formula_aw_mod import AWmod
    from formula_mpm import MPM
    from formula_rec13 import Rec13
    from sed_writer import SedWriter
except:
    print('ExceptionError: Cannot import own scripts.')


class MethodContainer(AW, AWmod, MPM, Rec13):
    # inherits functions from all sediment transport model classes
    # instantiate an object: A = Qs('method')
    # instantiate a new object for every method

    def __init__(self, method, input_dir, output_dir):
        try:            
            self.HEC = HEC1D(input_dir + 'HECRAS.csv')
            print(' * reading 1D (HECRAS) data from ' + input_dir + 'HECRAS.csv')
        except:
            try:
                self.HEC = HEC1D(input_dir + '/HECRAS.csv')
                print(' * reading 1D (HECRAS) data from: ' + input_dir + '/HECRAS.csv')
            except:
                print('ERROR: Cannot fint HECRAS.csv')
                print('       provided directory: ' + input_dir)

        self.method = str(method).lower()
        self.grains = GrainInfo(input_dir)
        self.grains()
        
       
        # initialize relevant method only
        self.writer = SedWriter(method, output_dir)
        if method == 'aw':
            self.calc = AW(input_dir)
        if method == 'awmod':
            self.calc = AWmod(input_dir)
        if method == 'mpm':
            self.calc = MPM(input_dir)
        if method == 'rec13':
            self.calc = Rec13(input_dir)

        self.method_dict = {'mpm': 'Meyer-Peter & Mueller (1948)',
                            'aw': 'Ackers & White (1973)',
                            'awmod': 'Ackers & White (1973) with modal solid transport',
                            'rec13': 'Recking (2013)'}
        self.Qb = np.ones((1, 1))
        self.Qmorph =np.ones((1, 1))
        self.kst = np.zeros((1, 1))
        self.warnings = []

    def compute_Qmorph(self, iP):
        Jm = np.mean(self.HEC.data[iP, :, 15])

        for g in range(0, self.grains.N):
            _hm = self.calc.compute_hmorph(Jm, g, self.kst[iP])  # based on mean energy slope and Dm

            # find position in h values
            if not np.isnan(_hm):
                _positions = np.where(self.HEC.data[iP, :, 6] > _hm)
            else:
                _positions = 'x'

            # hmorph is bigger than all discharge values
            if len(_positions[0]) == 0:
                self.Qmorph[iP, g] = self.HEC.data[iP, self.HEC.n_Q - 1, 3] * (
                            1 + (_hm - self.HEC.data[iP, self.HEC.n_Q - 1, 6]) / self.HEC.data[iP, self.HEC.n_Q - 1, 6])

            # hmorph is smaller than all discharge values
            if (len(_positions[0]) == self.HEC.n_Q) or (_positions == 'x'):
                self.Qmorph[iP, g] = np.nan

            # hmorph is within discharge values
            if (0 < len(_positions[0])) and (len(_positions[0]) < self.HEC.n_Q and not(_positions == 'x')):
                self.Qmorph[iP, g] = self.HEC.data[iP, _positions[0][0], 3] * (
                            1 + (_hm - self.HEC.data[iP, _positions[0][0], 6]) / (
                                self.HEC.data[iP, _positions[0][0], 6] - self.HEC.data[iP, _positions[0][0] - 1, 6]))

            if self.Qmorph[iP, g] < 0:
                self.Qmorph = np.nan

    def get_values(self, iP, jQ):
        Q = self.HEC.data[iP, jQ, 3]
        RhL = self.HEC.data[iP, jQ, 5]
        RhC = self.HEC.data[iP, jQ, 6]
        RhR = self.HEC.data[iP, jQ, 7]
        wL = self.HEC.data[iP, jQ, 8]
        wC = self.HEC.data[iP, jQ, 9]
        wR = self.HEC.data[iP, jQ, 10]
        uL = self.HEC.data[iP, jQ, 11]
        uC = self.HEC.data[iP, jQ, 12]
        uR = self.HEC.data[iP, jQ, 13]
        Fr = self.HEC.data[iP, jQ, 14]
        J = self.HEC.data[iP, jQ, 15]
        return Q, RhL, RhC, RhR, wL, wC, wR, uL, uC, uR, Fr, J

    def __call__(self):
        print('------->>> START PROCESSING')
        self.HEC()      # get HEC-RAS data
        self.Qb = np.nan * np.ones((self.HEC.n_prof, self.HEC.n_Q, self.grains.N))
        self.Qmorph = np.nan * np.ones((self.HEC.n_prof, self.grains.N))
        self.kst = np.zeros((self.HEC.n_prof, 1))

        for i in range(0, self.HEC.n_prof):
            print('------->>> Profile [River Sta]: ' + str(self.HEC.profile_names[i]))
            for j in range(0, self.HEC.n_Q):
                
                Q, RhL, RhC, RhR, wL, wC, wR, uL, uC, uR, Fr, J = self.get_values(i, j)
                print(' * discharge: ' + str(Q))
                _warnings = []

                for k in range(0, self.grains.N):
                    _warnings.append(self.calc.check_validity(J, self.grains.Dm[k], Q, RhC, Fr, k))
                    self.Qb[i, j, k] = self.calc(J, Q, RhL, RhC, RhR, wL, wC, wR, uL, uC, uR, Fr, k)
                self.calc.warnings.append(str(_warnings).strip('[]'))
                self.kst[i] = self.kst[i] + uC / (RhC ** (2 / 3) * J ** (1 / 2))
            self.kst[i] = self.kst[i] / self.HEC.n_Q
            self.compute_Qmorph(i)
        self.writer.write_summary(self.method_dict[self.method], self.HEC.profile_names, self.HEC.discharge_names, self.grains.g_names)
        self.writer.write_Qmorph(self.Qmorph, self.HEC.profile_names, self.grains.g_names)
        _Q = self.HEC.data[0, :, 3]
        self.writer.write_discharges(_Q, self.Qb, self.HEC.discharge_names, self.HEC.profile_names, self.grains.g_names, self.calc.warnings)
        self.writer.close_wb()
        print('------->>> Results written to ' + str(self.method) + '.xlsx  --- Finished.' )



