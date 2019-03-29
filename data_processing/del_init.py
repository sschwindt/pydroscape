import os, sys
print(sys.version)
print(sys.executable)

try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
except:
    pass

try:
    from d_launch import *
except:
    print("ERROR: Cannot access e_data scripts. Check installation.")

