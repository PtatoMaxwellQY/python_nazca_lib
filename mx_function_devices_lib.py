## This file is used for generating certain functional devices based on GDS files ##

from turtle import width
from matplotlib.pyplot import cla
import nazca as nd
import numpy as np
import nazca.interconnects as IC

import mx_gds_lib_load as mgl
import mx_frame_lib as mfl

class MZI :
    def __init__ (self,tapout,coupler_name,L=200,dL=0,R_bend=15,dy=10,w_heater=3):
        with nd.Cell(instantiate=False) as C:
                  
            dc_coupler = mgl.mx_lib_load(tapout.lib_path,coupler_name)
            sz_dc = [np.abs(dc_coupler.pin['a1'].x - dc_coupler.pin['b1'].x),np.abs(dc_coupler.pin['a1'].y - dc_coupler.pin['a2'].y)]
            width = np.abs(dc_coupler.pin['a1'].width)

            ic = IC.Interconnect(xs=tapout.XS_WG_RIB,width=width, radius=R_bend)

            dc_A = dc_coupler.put(-(L/2+R_bend*2+sz_dc[0]/2),0,0)
            dc_B = dc_coupler.put((L/2+R_bend*2+sz_dc[0]/2),0,0)

            nd.Pin(name='a1',pin=dc_A.pin['a1']).put()
            nd.Pin(name='a2',pin=dc_A.pin['a2']).put()             
            nd.Pin(name='b1',pin=dc_B.pin['b1']).put()
            nd.Pin(name='b2',pin=dc_B.pin['b2']).put()         
            
            _w_heater_ = tapout.W_METAL_MIN+3

            ## upper arm ##
            nd.bend(xs=tapout.XS_WG_RIB,radius=R_bend,width=width,angle=90).put('a0',dc_A.pin['b1'],flip=0)
            nd.strt(xs=tapout.XS_WG_RIB,length=dy+dL,width=width).put()
            up = nd.bend(xs=tapout.XS_WG_RIB,radius=R_bend,width=width,angle=90).put(flip=1)
            nd.strt(xs=tapout.XS_WG_RIB,length=L,width=width).put()
            temp = nd.bend(xs=tapout.XS_WG_RIB,radius=R_bend,width=width,angle=90).put(flip=1)
            ic.strt_bend_strt_p2p(pin1=temp.pin['b0'],pin2=dc_B.pin['a1']).put()

            up_heater = nd.strt(length=L,width=w_heater,xs=tapout.XS_HEATER).put('a0',up.pin['b0'])
            
            ## lower arm ## 
            nd.bend(xs=tapout.XS_WG_RIB,radius=R_bend,width=width,angle=90).put('a0',dc_A.pin['b2'],flip=1)
            nd.strt(xs=tapout.XS_WG_RIB,length=dy,width=width).put()
            down = nd.bend(xs=tapout.XS_WG_RIB,radius=R_bend,width=width,angle=90).put(flip=0)
            nd.strt(xs=tapout.XS_WG_RIB,length=L,width=width).put()
            temp = nd.bend(xs=tapout.XS_WG_RIB,radius=R_bend,width=width,angle=90).put(flip=0)
            ic.strt_bend_strt_p2p(pin1=temp.pin['b0'],pin2=dc_B.pin['a2']).put()
            down_heater = nd.strt(length=L,width=w_heater,xs=tapout.XS_HEATER).put('a0',down.pin['b0'])

            vtx_x = [-_w_heater_,0,_w_heater_/2,0,-_w_heater_]
            vtx_y = [_w_heater_/2,_w_heater_/2,0,-_w_heater_/2,-_w_heater_/2]

            vtx = np.c_[vtx_x,vtx_y]
            mfl._my_polygon(layer_wg=tapout.LAYER_METAL,vtx=vtx).put(up_heater.pin['a0'].x,up_heater.pin['a0'].y,0)
            mfl._my_polygon(layer_wg=tapout.LAYER_METAL,vtx=vtx).put(up_heater.pin['b0'].x,up_heater.pin['b0'].y,180)
            nd.Pin(name='e1',width=_w_heater_).put(up_heater.pin['a0'].x-_w_heater_,up_heater.pin['a0'].y,up_heater.pin['a0'].a)
            nd.Pin(name='e2',width=_w_heater_).put(up_heater.pin['b0'].x+_w_heater_,up_heater.pin['b0'].y,up_heater.pin['b0'].a)

            mfl._my_polygon(layer_wg=tapout.LAYER_METAL,vtx=vtx).put(down_heater.pin['a0'].x,down_heater.pin['a0'].y,0)
            mfl._my_polygon(layer_wg=tapout.LAYER_METAL,vtx=vtx).put(down_heater.pin['b0'].x,down_heater.pin['b0'].y,180)
            nd.Pin(name='e3',width=_w_heater_).put(down_heater.pin['a0'].x-_w_heater_,down_heater.pin['a0'].y,down_heater.pin['a0'].a)
            nd.Pin(name='e4',width=_w_heater_).put(down_heater.pin['b0'].x+_w_heater_,down_heater.pin['b0'].y,down_heater.pin['b0'].a)           
            

        self.cell = C

class Grating:
    def __init__ (self,tapout,grating_name):
        with nd.Cell(instantiate=False) as C:
            grating = mgl.mx_lib_load(tapout.lib_path,grating_name).put(0,0,90)
            nd.Pin(name='g0',pin=grating.pin['g0']).put()         
        self.cell = C

