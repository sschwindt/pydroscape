import os, sys
print(sys.version)
print(sys.executable)

try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
except:
    pass

try:
    import c_plot as e_plot
    import c_xlsx as e_xlsx    
    
except:
    print("ERROR: Cannot access own scripts. Check installation and write rights.")




