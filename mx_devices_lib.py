from unicodedata import name
import nazca as nd
import numpy as np

import mx_frame_lib as mfl
import mx_structure_lib as msl

## notice : layers is the rang of all layers ##
class my_std_ring_resonator :
    def __init__ (self,tapout,radius=10,width=0.45,coupler1_angle=0,coupler1_width=0.45,gap1=0.45,w_heater=3.5,wg_type='strip',coupler2_angle=0,coupler2_width=0,gap2=0.45):
        with nd.Cell(instantiate=False) as C:
            if wg_type == 'rib' and ('tapout.XS_WG_RIB' in   locals().keys()) :
                xs_wg = tapout.XS_WG_RIB
            else :
                xs_wg = tapout.XS_WG_STRIP
            
            ## adding the major ring ##
            nd.bend(xs=xs_wg,radius=radius,width=width,angle=360).put(0,-radius,0)

            ## The lower coupling bus ##
            _radius_coupler_ = radius+width/2+gap1+coupler1_width/2
            nd.bend(xs=xs_wg,radius=_radius_coupler_,width=coupler1_width,angle=coupler1_angle/2).put(0,-_radius_coupler_,0)
            nd.bend(xs=xs_wg,radius=_radius_coupler_,width=coupler1_width,angle=coupler1_angle/2).put(flip=1)
            temp = nd.strt(xs=xs_wg,length=10,width=coupler1_width).put(flip=0)
            nd.Pin(name='b1',pin=temp.pin['b0']).put()

            nd.bend(xs=xs_wg,radius=_radius_coupler_,width=coupler1_width,angle=coupler1_angle/2).put(0,-_radius_coupler_,180,flip=1)
            nd.bend(xs=xs_wg,radius=_radius_coupler_,width=coupler1_width,angle=coupler1_angle/2).put(flip=0)
            temp = nd.strt(xs=xs_wg,length=10,width=coupler1_width).put(flip=0)
            nd.Pin(name='a1',pin=temp.pin['b0']).put()

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

# =================================================================
# @ File : <mx_devices_lib.py>
# @ Device: Strip Heater
# @ Parameters : * tapout   :[ select your tapout foundary: found in <layer_definition.py>]
#              : * w_heater : width of the heater, default 3.5um
#              : * L        : Length of the heater, default 200um
#              : * w_metal  : width of the attaching metal routing, default 8um
# =================================================================
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

# =================================================================
# @ File : <mx_devices_lib.py>
# @ Device: Racetrack with Euler bends
# @ Parameters : * tapout   :[ select your tapout foundary: found in <layer_definition.py>]
#              : * w_heater : width of the heater, default 3.5um
#              : * L        : Length of the heater, default 200um
#              : * w_metal  : width of the attaching metal routing, default 8um
# =================================================================
class my_crow_euler_bend_racetrack :
    def __init__ (self,tapout,gaps,w1,w0,R1,R0,R2,w_cp,w_wg,dC,cp_type='BDC',heater_type='connected',w_heater=3.5,dLx=0,dLy=0):
        with nd.Cell(instantiate=False) as C:
            order = len(gaps) - 1 # the order of the crow

            if (len(w1)==1):
                w1 = w1*np.ones((len(gaps)))
                w0 = w0*np.ones((len(gaps)))
                R1 = R1*np.ones((len(gaps)))
                R0 = R0*np.ones((len(gaps)))
                R2 = R2*np.ones((len(gaps)))
                dLx = dLx*np.ones((len(gaps)))
                dLy = dLy*np.ones((len(gaps)))

            idx = np.linspace(0,order-1,order)
            _y_init_ = gaps[0]/2+w_cp/2
            ## generating the rings ##

            rack_pre = msl.my_racetrack_euler_bend(layer_wg=tapout.LAYER_WG_RIB,w1=w1[0],w0=w0[0],R1=R1[0],R0=R0[0],R2=R2[0],dLx=dLx[0],dLy=dLy[0])

            for _idx_ in idx:
                _idx_ = int(_idx_)
                rack_cur = msl.my_racetrack_euler_bend(layer_wg=tapout.LAYER_WG_RIB,w1=w1[_idx_],w0=w0[_idx_],R1=R1[_idx_],R0=R0[_idx_],R2=R2[_idx_],dLx=dLx[_idx_],dLy=dLy[_idx_])
                _y_rack_ = _y_init_ + rack_cur.sz[1]/2 +w0[_idx_]/2+gaps[_idx_]/2
                rack_cur.cell.put(0,_y_rack_ ,0)
                _y_init_ = _y_init_ + rack_cur.sz[1] + w0[_idx_] + gaps[_idx_+1]/2 + gaps[_idx_]/2
                if (w_heater!=0):
                    _r_heater_ = rack_cur.sz[0]/2
                    mfl.my_std_ring(layer=tapout.LAYER_HEATER,radius=_r_heater_,width=w_heater,theta_start=135, theta_stop=180).frame.put(-dLx[_idx_]/2,_y_rack_+dLy[_idx_]/2,0)
                    mfl.my_std_ring(layer=tapout.LAYER_HEATER,radius=_r_heater_,width=w_heater,theta_start=180, theta_stop=225).frame.put(-dLx[_idx_]/2,_y_rack_-dLy[_idx_]/2,0)
                    mfl.my_std_ring(layer=tapout.LAYER_HEATER,radius=_r_heater_,width=w_heater,theta_start=0, theta_stop=45).frame.put(dLx[_idx_]/2,_y_rack_+dLy[_idx_]/2,0)
                    mfl.my_std_ring(layer=tapout.LAYER_HEATER,radius=_r_heater_,width=w_heater,theta_start=-45, theta_stop=0).frame.put(dLx[_idx_]/2,_y_rack_-dLy[_idx_]/2,0)
                    nd.strt(length=dLy[_idx_],width=w_heater,layer=tapout.LAYER_HEATER).put(-dLx[_idx_]/2-_r_heater_,_y_rack_-dLy[_idx_]/2,90)
                    nd.strt(length=dLy[_idx_],width=w_heater,layer=tapout.LAYER_HEATER).put( dLx[_idx_]/2+_r_heater_,_y_rack_-dLy[_idx_]/2,90)
                    if (heater_type=='connected'):
                        if (_idx_==0): # starting ring
                            _L_attach_heater_ = 3*w_heater
                            _x_attach_ = -dLx[_idx_]/2-_r_heater_*np.cos(np.pi/4)-(1-np.cos(np.pi/4))*w_heater/2
                            _y_attach_ = _y_rack_-dLy[_idx_]/2-_r_heater_*np.sin(np.pi/4)+w_heater*np.sin(np.pi/4)/2
                            h_dl = nd.strt(length=_L_attach_heater_,width=w_heater,layer=tapout.LAYER_HEATER).put(_x_attach_,_y_attach_,-90)
                            h_dr = nd.strt(length=_L_attach_heater_,width=w_heater,layer=tapout.LAYER_HEATER).put(-_x_attach_,_y_attach_,-90)
                        else:
                            _L_attach_heater_ = rack_cur.sz[1]/2-dLy[_idx_]/2- _r_heater_*np.cos(np.pi/4) + w0[_idx_]/2+gaps[_idx_]/2 +w_heater/2
                            _x_attach_ = -dLx[_idx_]/2-_r_heater_*np.cos(np.pi/4)-(1-np.cos(np.pi/4))*w_heater/2
                            _y_attach_ = _y_rack_-dLy[_idx_]/2-_r_heater_*np.sin(np.pi/4)+w_heater*np.sin(np.pi/4)/2
                            nd.strt(length=_L_attach_heater_,width=w_heater,layer=tapout.LAYER_HEATER).put(_x_attach_,_y_attach_,-90)
                            nd.strt(length=_L_attach_heater_,width=w_heater,layer=tapout.LAYER_HEATER).put(-_x_attach_,_y_attach_,-90)

                        if (_idx_==order-1): # starting ring
                            _L_attach_heater_ = 3*w_heater
                        else:
                            _L_attach_heater_ = rack_cur.sz[1]/2-dLy[_idx_]/2- _r_heater_*np.cos(np.pi/4) + w0[_idx_]/2+gaps[_idx_]/2 +w_heater/2
                        _x_attach_ = -dLx[_idx_]/2-_r_heater_*np.cos(np.pi/4)-(1-np.cos(np.pi/4))*w_heater/2
                        _y_attach_ = _y_rack_+dLy[_idx_]/2+_r_heater_*np.sin(np.pi/4)-w_heater*np.sin(np.pi/4)/2
                        h_ul = nd.strt(length=_L_attach_heater_,width=w_heater,layer=tapout.LAYER_HEATER).put(_x_attach_,_y_attach_,90)
                        h_ur = nd.strt(length=_L_attach_heater_,width=w_heater,layer=tapout.LAYER_HEATER).put(-_x_attach_,_y_attach_,90)
            
            if (w_heater!=0):
                nd.strt(width=tapout.W_METAL_MIN,layer=tapout.LAYER_METAL,length=np.abs(h_ul.pin['b0'].x-h_ur.pin['b0'].x)+w_heater).put(h_ul.pin['b0'].x-w_heater/2,h_ul.pin['b0'].y-tapout.W_METAL_MIN/2,0)    
                mtl = nd.strt(width=tapout.W_METAL_MIN,layer=tapout.LAYER_METAL,length=2*tapout.W_METAL_MIN).put(h_dl.pin['b0'].x+w_heater/2,h_dl.pin['b0'].y+tapout.W_METAL_MIN/2,180)    
                mtr = nd.strt(width=tapout.W_METAL_MIN,layer=tapout.LAYER_METAL,length=2*tapout.W_METAL_MIN).put(h_dr.pin['b0'].x-w_heater/2,h_dr.pin['b0'].y+tapout.W_METAL_MIN/2,0)    
                nd.Pin(name='e1',pin=mtl.pin['b0']).put()
                nd.Pin(name='e2',pin=mtr.pin['b0']).put()
            if cp_type=='BDC' or cp_type=='bend' or cp_type=='b':
                R_cp = R0[0]+w0[0]/2+gaps[0]+w_cp/2
                #c_attach = dC/2 + (np.pi-dC/2)/2
                c_attach = np.pi/4
                cp_d = msl.my_euler_coupler(layer_wg=tapout.LAYER_WG_RIB,w_wg=w_wg,w_cp=w_cp,Rmax=15,R_cp=R_cp,dLc=0,dAc=dC,theta_attach=c_attach,coupler_type = 'BDC').cell.put(0,0,0)
                cp_u = msl.my_euler_coupler(layer_wg=tapout.LAYER_WG_RIB,w_wg=w_wg,w_cp=w_cp,Rmax=15,R_cp=R_cp,dLc=0,dAc=dC,theta_attach=c_attach,coupler_type = 'BDC').cell.put(0,_y_init_+ w_cp/2+gaps[-1]/2,0,flip=1)

            nd.Pin(name='a1',pin=cp_u.pin['a1']).put()
            nd.Pin(name='a2',pin=cp_d.pin['a1']).put()
            nd.Pin(name='b1',pin=cp_u.pin['b1']).put()
            nd.Pin(name='b2',pin=cp_d.pin['b1']).put()
            ## generating the coupler ##
            

        self.cell = C
 
