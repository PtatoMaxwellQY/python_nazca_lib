import nazca as nd
import numpy as np

#### Load the gds lib as a cell ####
def mx_lib_load(lib_path,lib_name):

    with nd.Cell(instantiate= False) as lib_cell:
        f = open(lib_path+lib_name+'.txt',"r") 
        str = f.read() 
        exec(str)
        f.close()
        nd.load_gds(filename=lib_path+lib_name+'.gds').put(0,0,0)
    return lib_cell




