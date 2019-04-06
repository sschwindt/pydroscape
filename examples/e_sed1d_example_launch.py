#!/usr/bin/python
# Instruction: Compute solid discharge based on HEC-RAS computation
#          > Header definition of HEC-RAS file:
#            REACH[1-name] RIVERsTA[2-m] PROFILE[3-Qname] QtOTAL[4m3s] MINcHeL[5-m]
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\..')))
import pydroscape.e_sed1d as pss


def main(method):
    sediment_container = pss.SedimentTransport1D(True)  # the BOOL=False argument initiates e_sed1D with messages (silence=False)
    sediment_container.set_input_file_directory(os.path.dirname(__file__) + '/sample_data/text/sediment_calculation_1D/')
    sediment_container.set_output_file_directory(os.path.dirname(__file__) + '/output/')
    sediment_container.calculate(method)


if __name__ == '__main__':
    # prompt sediment transport calculation method
    method = str(input('Please enter solid transport formula (AW, AWmod, MPM, Rec13) \n>> '))
    main(method)
