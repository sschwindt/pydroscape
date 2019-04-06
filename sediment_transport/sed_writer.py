#!/usr/bin/python
import sys, os
import numpy as np
sys.path.append(os.path.dirname(__file__))
import xlsxwriter as xsw


class SedWriter:
    # This class stores all information about the treated measurement files.
    # for details, refer to http://xlsxwriter.readthedocs.org/index.html
    def __init__(self, wb_name, directory):
        try:
            self.wb = xsw.Workbook(directory + wb_name + '.xlsx')
            print(' * Results Workbook: ' + directory + wb_name + '.xlsx')
        except:
            try:
                self.wb = xsw.Workbook(directory + '/' + wb_name + '.xlsx')
                print(' * Results Workbook: ' + '/' + directory + wb_name + '.xlsx')
            except:
                self.wb = xsw.Workbook(wb_name + '.xlsx')
                print(' * Results Workbook: ' + wb_name + '.xlsx')
        self.wb_format = self.wb.add_format()
        self.wb_format.set_font_name('Times New Roman')
        self.wb_formatQ = self.wb.add_format()
        self.wb_formatQ.set_num_format('00.0')
        self.wb_formatQ.set_bold()
        self.wb_formatQ.set_italic()

        self.wb_formatQb = self.wb.add_format()
        self.wb_formatQb.set_num_format('0.00')

        self.wb_format_bold = self.wb.add_format()
        self.wb_format_bold.set_bold()

        self.wb_format_italic = self.wb.add_format()
        self.wb_format_italic.set_italic()

        self.wb_format0val = self.wb.add_format()
        self.wb_format0val.set_font_color('blue')
        self.wb_format0val.set_bg_color('gray')

        self.sh_summary = self.wb.add_worksheet()
        self.sh_Qmorph = self.wb.add_worksheet()
        self.sh_Q = self.wb.add_worksheet()

    def close_wb(self):
        self.wb.close()

    def write_discharges(self, Q, Qb, Q_names, prof_names, grain_names, warnings):
        self.sh_Q.name = 'Discharge analysis'
        nQ = len(Qb[0, :, 0])
        nP = len(Qb[:, 0, 0])
        nD = len(Qb[0, 0, :])

        for q in range(0, nQ):
            start_row = 2 + q * (3 + nP + 2)
            self.sh_Q.set_comments_author('Warning generator')
            self.sh_Q.write('B' + str(start_row), 'Discharge:', self.wb_formatQ)
            self.sh_Q.write('C' + str(start_row), Q_names[q] + ' = ', self.wb_formatQ)
            self.sh_Q.write('D' + str(start_row), Q[q], self.wb_formatQ)
            self.sh_Q.write('E' + str(start_row), '[m3/s]', self.wb_formatQ)
            self.sh_Q.write('B' + str(start_row + 1), 'Profile', self.wb_format_bold)
            self.sh_Q.write('B' + str(start_row + 2), '[River Sta]', self.wb_format_italic)
            for gD in range(0, nD):
                self.sh_Q.write(chr(2 + gD + ord('A')) + str(start_row + 1), 'Qs ({0})'.format(grain_names[gD]), self.wb_format_bold)
                self.sh_Q.write(chr(2 + gD + ord('A')) + str(start_row + 2), '[kg/s]', self.wb_format_italic)
                self.sh_Q.set_column(2 + gD, 2 + gD, 15)
            for p in range(0, nP):
                self.sh_Q.write_comment('B' + str(start_row + 3 + p), warnings[nP * q + p], {'x_scale': 1.2, 'y_scale': 0.8})
                self.sh_Q.write('B' + str(start_row + 3 + p), prof_names[p])
                for g in range(0, nD):
                    if not (Qb[p, q, g] == 0 or np.isnan(Qb[p, q, g]) or np.isinf(Qb[p, q, g])):
                        self.sh_Q.write(chr(2 + g + ord('A')) + str(start_row + 3 + p), Qb[p, q, g], self.wb_formatQb)
                    else:
                        self.sh_Q.write(chr(2 + g + ord('A')) + str(start_row + 3 + p), '', self.wb_format0val)

    def write_Qmorph(self, Qmorph, prof_names, grain_names):
        self.sh_Qmorph.name = 'Incipient motion'
        self.sh_Qmorph.write('B2', 'Discharge for incipient motion (Qini) based on Dm.')
        self.sh_Qmorph.write('B4', 'Profile', self.wb_format_bold)
        self.sh_Qmorph.write('B5', '[River Sta]', self.wb_format_italic)
        for gD in range(0, len(grain_names)):
            _col = 2+gD
            self.sh_Qmorph.write(chr(_col + ord('A')) + str(4), 'Qini ({0})'.format(grain_names[gD]), self.wb_format_bold)
            self.sh_Qmorph.write(chr(_col + ord('A')) + str(5), '[m3/s]', self.wb_format_italic)
            self.sh_Qmorph.set_column(_col, 2 + gD, 20)
            for p in range(0, len(prof_names)):
                if gD == 0:
                    cell_address = 'B' + str(6 + p)
                    self.sh_Qmorph.write(cell_address, prof_names[p], self.wb_formatQb)
                cell_address = chr((2 + gD) + ord('A')) + str(6 + p)
                if not (Qmorph[p, gD] == 0 or np.isnan(Qmorph[p, gD]) or np.isinf(Qmorph[p, gD])):
                    self.sh_Qmorph.write(cell_address, Qmorph[p, gD])
                else:
                    self.sh_Qmorph.write(cell_address, '', self.wb_format0val)

    def write_summary(self, method_name, prof_names, Q_names, grain_names):
        self.sh_summary.name = 'Summary'
        self.sh_summary.set_column(1, 3, 23)  # adjust the column width (startcol[A=0!], endCol, pt.Value)

        self.sh_summary.write('B2', 'Solid discharge formula:')
        self.sh_summary.write('C2', method_name)

        self.sh_summary.write('B4', 'Profiles', self.wb_format_bold)
        self.sh_summary.write('C4', 'Discharges', self.wb_format_bold)
        self.sh_summary.write('D4', 'Grain size distributions', self.wb_format_bold)

        Q_names = np.flipud(Q_names)
        for i in range(0, len(prof_names)):
            self.sh_summary.write('B' + str(5 + i), prof_names[i])
        for i in range(0, len(Q_names)):
            self.sh_summary.write('C' + str(5 + i), Q_names[i])
        for i in range(0, len(grain_names)):
            self.sh_summary.write('D' + str(5 + i), grain_names[i])

    def __call__(self):
        pass






