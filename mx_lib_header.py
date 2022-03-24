## head files ##
import nazca as nd
import numpy as np

## finding the system path of the library ##
# import os,sys
# sys.path.append("G:\\OneDrive\\OneDrive - The Chinese University of Hong Kong\\Library\\mx_git\\python\\nazca_libs")

import mx_frame_lib as mfl
import mx_devices_lib as mdl
import mx_function_devices_lib as mfdl
import mx_gds_lib_load as mgl

####################### File : <mx_frame_lib> #######################
def mx_polygon (layer_wg,vtx):
    frame = mfl._my_polygon (layer_wg,vtx)
    return frame

def mx_poly_spiral(r,theta,coord,order,dL,R_max):
    return mfl.my_poly_spiral(r,theta,coord,order,dL,R_max)

class mx_std_ring(mfl.my_std_ring) :
    def __init__(self, layer = 1,radius = 10, width = 0.45,theta_start = 0, theta_stop=360, n_points = 1024):
        super(mx_std_ring, self).__init__(layer,radius,width,theta_start,theta_stop,n_points)

class mx_std_racetrack(mfl.my_std_racetrack) :
    def __init__(self,layer=1,radius=10,L1=5,L2=5,width =0.45,n_points =256):
        super(mx_std_racetrack, self).__init__(layer,radius,L1,L2,width,n_points)   

class mx_poly_wg(mfl.poly_wg):
    def __init__(self,vtx_line,width):
        super(mx_poly_wg,self).__init__(vtx_line,width)

####################### File : <mx_devices_lib> #######################
class mx_std_ring_resonator(mdl.my_std_ring_resonator) :
    def __init__(self,tapout,radius=10,width=0.45,coupler1_angle=0,coupler1_width=0.45,gap1=0.45,w_heater=3.5,wg_type='rib',slab_width=4,coupler2_angle=0,coupler2_width=0,gap2=0.45):
        super(mx_std_ring_resonator, self).__init__(tapout,radius,width,coupler1_angle,coupler1_width,gap1,w_heater,wg_type,slab_width,coupler2_angle,coupler2_width,gap2)   

class mx_strip_heater(mdl.my_strip_heater) :
    def __init__ (self,tapout,w_heater=3.5,L=200,w_metal=8):
        super(mx_strip_heater, self).__init__(tapout,w_heater,L,w_metal)   

####################### File : <mx_function_devices> #######################
class mx_MZI(mfdl.MZI) :
    def __init__(self,tapout,coupler_name='xhn_3db_tdc',L=200,dL=0,R_bend=15,dy=10,w_heater=3):
        super(mx_MZI, self).__init__(tapout,coupler_name,L,dL,R_bend,dy,w_heater)   

class mx_Grating(mfdl.Grating):
    def __init__(self,tapout,coupler_name='xhn_grtcp_swg'):
        super(mx_Grating, self).__init__(tapout,coupler_name)   

class mx_crow_euler_bend_racetrack(mdl.my_crow_euler_bend_racetrack):
    def __init__ (self,tapout,gaps,w1,w0,R1,R0,dLx,dLy,w_heater):
        super(mx_crow_euler_bend_racetrack,self).__init__(tapout,gaps,w1,w0,R1,R0,dLx,dLy,w_heater)

####################### File : <mx_gds_lib_load> #######################
def mx_gds_lib_load(lib_path,lib_name):
    return mgl.mx_lib_load(lib_path,lib_name)



class mx_PADs:
    def __init__(self,tapout,num,length=80,width=60,edge=5,rows=1,x_spacing=100,y_spacing=120):
        with nd.Cell(instantiate=False) as C: 
            idx = np.linspace(0,num-1,num)
            row_idx = np.linspace(0,rows-1,rows)
            for _row_ in row_idx:
                for _idx_ in idx:
                    _pad_ = nd.strt(length=length,width=width,layer=tapout.LAYER_METAL_PAD).put(_idx_*x_spacing + _row_*x_spacing/2,-length/2 - _row_*y_spacing ,90)
                    nd.Pin(name='e'+str(int(_idx_*rows+_row_+1)),pin=_pad_.pin['b0']).put()
                    nd.strt(length=length+2*edge,width=width+2*edge,layer=tapout.LAYER_METAL).put(_idx_*x_spacing + _row_*x_spacing/2,-length/2-edge - _row_*y_spacing,90)

        self.cell = C


