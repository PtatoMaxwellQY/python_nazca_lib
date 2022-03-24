from unicodedata import name
import nazca as nd
import numpy as np

import mx_frame_lib as mfl
import mx_structure_lib as msl

## notice : layers is the rang of all layers ##
class my_std_ring_resonator :
    def __init__ (self,tapout,radius=10,width=0.45,coupler1_angle=0,coupler1_width=0.45,gap1=0.45,w_heater=3.5,wg_type='rib',slab_width=4,coupler2_angle=0,coupler2_width=0,gap2=0.45):
        with nd.Cell(instantiate=False) as C:
            if wg_type == 'slab' and ('tapout.XS_WG_SLAB' in   locals().keys()) :
                xs_wg = tapout.XS_WG_SLAB
            else :
                xs_wg = tapout.XS_WG_RIB
            
            ## adding the major ring ##
            nd.bend(xs=xs_wg,radius=radius,width=width,angle=360).put(0,-radius,0)

            ## The lower coupling bus ##
            _radius_coupler_ = radius+width/2+gap1+coupler1_width/2
            nd.bend(xs=xs_wg,radius=_radius_coupler_,width=coupler1_width,angle=coupler1_angle/2).put(0,-_radius_coupler_,0)
            nd.bend(xs=xs_wg,radius=_radius_coupler_,width=coupler1_width,angle=coupler1_angle/2).put(flip=1)
            temp = nd.strt(xs=xs_wg,length=10,width=coupler1_width).put(flip=0)
            nd.Pin(name='a1',pin=temp.pin['b0']).put()

            nd.bend(xs=xs_wg,radius=_radius_coupler_,width=coupler1_width,angle=coupler1_angle/2).put(0,-_radius_coupler_,180,flip=1)
            nd.bend(xs=xs_wg,radius=_radius_coupler_,width=coupler1_width,angle=coupler1_angle/2).put(flip=0)
            temp = nd.strt(xs=xs_wg,length=10,width=coupler1_width).put(flip=0)
            nd.Pin(name='b1',pin=temp.pin['b0']).put()

            _heater_upper_ = 90
            _theta_end_ = 55

            ## The upper coupling bus ##
            if coupler2_width >0:
                nd.bend(xs=xs_wg,radius=radius,width=width,angle=360).put(0,-radius,0)
                _radius_coupler_ = radius+width/2+gap1+coupler2_width/2
                nd.bend(xs=xs_wg,radius=_radius_coupler_,width=coupler2_width,angle=coupler2_angle/2).put(0, _radius_coupler_,0,flip=1)
                nd.bend(xs=xs_wg,radius=_radius_coupler_,width=coupler2_width,angle=coupler2_angle/2).put(flip=0)
                temp = nd.strt(xs=xs_wg,length=10,width=coupler1_width).put(flip=0)
                nd.Pin(name='a2',pin=temp.pin['b0']).put()

                nd.bend(xs=xs_wg,radius=_radius_coupler_,width=coupler2_width,angle=coupler2_angle/2).put(0, _radius_coupler_,180,flip=0)
                nd.bend(xs=xs_wg,radius=_radius_coupler_,width=coupler2_width,angle=coupler2_angle/2).put(flip=1)
                temp = nd.strt(xs=xs_wg,length=10,width=coupler1_width).put(flip=0)
                nd.Pin(name='b2',pin=temp.pin['b0']).put()
                _heater_upper_ = 180 - _theta_end_
            
            mfl.my_std_ring(layer=tapout.LAYER_HEATER,radius=radius,width=w_heater,theta_start=_heater_upper_,theta_stop=180+_theta_end_).frame.put(0,0,0)
            mfl.my_std_ring(layer=tapout.LAYER_HEATER,radius=radius,width=w_heater,theta_start=-_theta_end_,theta_stop=180-_heater_upper_).frame.put(0,0,0)
            
            if coupler2_width >0:
                pad_c = nd.strt(length=radius*2*np.cos(45/180*np.pi),width=8,layer=tapout.LAYER_METAL).put(-radius*np.cos(45/180*np.pi),4+radius*np.sin(45/180*np.pi),0)


            pad_l = nd.strt(length=8,width=8,layer=tapout.LAYER_METAL).put(4-radius*np.cos(45/180*np.pi),-radius*np.sin(45/180*np.pi),-90)
            pad_r = nd.strt(length=8,width=8,layer=tapout.LAYER_METAL).put(-4+radius*np.cos(45/180*np.pi),-radius*np.sin(45/180*np.pi),-90)
            nd.Pin(name='e1',pin=pad_l.pin['b0']).put()
            nd.Pin(name='e2',pin=pad_r.pin['b0']).put()

        self.cell = C


class my_strip_heater :
    def __init__ (self,tapout,w_heater=3.5,L=200,w_metal=8):
        with nd.Cell(instantiate=False) as C:

            heater = nd.strt(length=L,width=w_heater,xs=tapout.XS_HEATER).put(-L/2,0,0)
            vtx_x = [-w_metal,0,w_metal/2,0,-w_metal]
            vtx_y = [w_metal/2,w_metal/2,0,-w_metal/2,-w_metal/2]

            vtx = np.c_[vtx_x,vtx_y]
            mfl._my_polygon(layer_wg=tapout.LAYER_METAL,vtx=vtx).put(heater.pin['a0'].x,heater.pin['a0'].y,0)
            mfl._my_polygon(layer_wg=tapout.LAYER_METAL,vtx=vtx).put(heater.pin['b0'].x,heater.pin['b0'].y,180)
            nd.Pin(name='e1',width=w_metal).put(heater.pin['a0'].x-w_metal,heater.pin['a0'].y,heater.pin['a0'].a)
            nd.Pin(name='e2',width=w_metal).put(heater.pin['b0'].x+w_metal,heater.pin['b0'].y,heater.pin['b0'].a)
        
        self.cell = C

class my_crow_euler_bend_racetrack :
    def __init__ (self,tapout,gaps,w1,w0,R1,R0,dLx,dLy,w_heater):
        with nd.Cell(instantiate=False) as C:
            order = len(gaps) - 1 # the order of the crow

            if (len(w1)==1):
                w1 = w1*np.ones((len(gaps)))
                w0 = w0*np.ones((len(gaps)))
                R1 = R1*np.ones((len(gaps)))
                R0 = R0*np.ones((len(gaps)))
                dLx = dLx*np.ones((len(gaps)))
                dLy = dLy*np.ones((len(gaps)))

            idx = np.linspace(0,order-1,order)
            _y_init_ = gaps[0]/2
            ## generating the rings ##
            for _idx_ in idx:
                _idx_ = int(_idx_)
                rack_temp = msl.my_racetrack_euler_bend(layer_wg=tapout.LAYER_WG_RIB,w1=w1[_idx_],w0=w0[_idx_],R1=R1[_idx_],R0=R0[_idx_],dLx=dLx[_idx_],dLy=dLy[_idx_])
                rack_temp.cell.put(0,_y_init_ + rack_temp.sz[1]/2 +w0[_idx_]/2 ,0)
                _y_init_ = _y_init_ + rack_temp.sz[1] + w0[_idx_] + gaps[_idx_+1]/2 + gaps[_idx_]/2
            msl.my_euler_coupler(layer_wg=tapout.LAYER_WG_RIB,Win=0.45,W_couple=0.376,Rmax=15,R_couple=10.5,dLc=0,dtheta=np.pi/5,theta_attach=np.pi/4,coupler_type = 'DC').cell.put(0,0,0)
            ## generating the coupler ##
            


        self.cell = C
 
