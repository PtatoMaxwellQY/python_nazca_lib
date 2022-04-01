## structure lib ##

from turtle import shape
import nazca as nd
import numpy as np

import mx_frame_lib as mfl
    

# =================================================================
# @ File : <mx_structure_lib.py>
# @ Device: Euler bending units
# @ Parameters : * layer_wg : the layer where the bend is located, only single layer
#              : * R0,R1    : curvature of the starting/ [ending/middle] ports
#              : * w0,w1    : width of the starting/ [ending/middle] ports
#              : * bend_angle : the direction angle of output differ from input port
#              : * bend_angle : the direction angle of output differ from input port
#              : * bend_type  : 'single' -- the bend curvature R0->R1
#                             : 'dual'   -- the bend curvature R0->R1->R0
#              : * width_type : 'sin'/'cos' -- w0->w1 varies with the angle of the points in the curve
#                             : 'linear'/default -- w0->w1 varies with the length of the curve linearly
# =================================================================

class my_euler_wg2wg:
    def __init__ (self,layer_wg=1,R0=10,R1=5,R2=10,Win=0.45,dW=0.15,bend_angle=np.pi/2,theta_start=0,coord_start=[0,0],bend_type='dual',width_type='cos'):
        with nd.Cell (instantiate=False) as C:
            if (bend_type=='single'):
                vtx_start = mfl.my_poly_spiral([R0,R1],[theta_start,bend_angle+theta_start],coord_start,1,0.001,1000)
                p_start = vtx_start[0,:]
                p_end = vtx_start[-1,:]
                vtx_euler_bend = vtx_start
            else :
                vtx_start = mfl.my_poly_spiral([R0,R1],[theta_start,bend_angle/2+theta_start],coord_start,1,0.001,1000)
                vtx_stop = mfl.my_poly_spiral([R1,R2],[bend_angle/2+theta_start,bend_angle+theta_start],[vtx_start[-1,0],vtx_start[-1,1]],1,0.001,1000)
                p_start = vtx_start[0,:]
                p_end = vtx_stop[-1,:]
                _len_ = int(len(vtx_stop[:,1]))
                vtx_euler_bend = np.r_[vtx_start,vtx_stop[1:_len_,:]] ## attaching waveguide 

            dx = np.abs(p_end[0] - p_start[0]) ## displacement in x direction

            _len_ = int(len(vtx_euler_bend[:,1]))
            dL = np.power((vtx_euler_bend[1:_len_,1] - vtx_euler_bend[0:_len_-1,1]),2) + np.power((vtx_euler_bend[1:_len_,0] - vtx_euler_bend[0:_len_-1,0]),2)
            dL = np.sqrt(dL)
            L = np.cumsum(dL) ## L for each pieces
            L = np.r_[[0],L]

            L0 = sum(dL)

            if (width_type=='cos'):## in this situation, dW is the difference of input and output
                dy = np.abs(p_end[1] - p_start[1]) ## displacement in y direction
                vtx_euler_bend[:,1] = -dy + vtx_euler_bend[:,1]
                z = vtx_euler_bend[:,0] + 1j*vtx_euler_bend[:,1]
                w = dW/2*np.cos(np.angle(z,deg=0)*np.pi/np.abs(bend_angle)) + (Win*2+dW)/2
            elif (width_type=='sin'): ## in this situation, win = wout, dW is the middle width difference
                dy = np.abs(vtx_start[-1,1] - vtx_start[0,1]) ## displacement in y direction
                vtx_euler_bend[:,1] = -dy + vtx_euler_bend[:,1]
                z = vtx_euler_bend[:,0] + 1j*vtx_euler_bend[:,1]
                w = dW/2*np.sin(np.angle(z,deg=0)*np.pi/np.abs(bend_angle)) + Win

            elif (width_type=='linear'):
                w = dW/L0*L + Win

            elif (width_type=='dual_linear'):
                w = dW/L0/2*np.abs(L-L0/2) + Win

            else : ## default linear from input to output
                w = dW/L0*L + Win

            euler_bend = mfl.poly_wg(vtx_euler_bend,w)
            mfl._my_polygon(layer_wg,euler_bend.vtx).put(0,0,0)
            nd.Pin(name='a0',width=w[0]).put(vtx_euler_bend[0,0],vtx_euler_bend[0,1],180+theta_start/np.pi*180)
            nd.Pin(name='b0',width=w[-1]).put(vtx_euler_bend[-1,0],vtx_euler_bend[-1,1],(theta_start/np.pi*180+bend_angle/np.pi*180))
            
        self.sz = [np.abs(p_end[0] - p_start[0]),np.abs(p_end[1] - p_start[1])]
        self.cell = C

# =================================================================
# @ File : <mx_structure_lib.py>
# @ Device: Racetracks with euler bends
# @ Parameters : * layer_wg : the layer where the bend is located, only single layer
#              : * R0,R1    : curvature of the starting/ [ending/middle] ports
#              : * w0,w1    : width of the starting/ [ending/middle] ports
#              : * bend_angle : the direction angle of output differ from input port
#              : * bend_angle : the direction angle of output differ from input port
#              : * bend_type  : 'single' -- the bend curvature R0->R1
#                             : 'dual'   -- the bend curvature R0->R1->R0
#              : * width_type : 'sin'/'cos' -- w0->w1 varies with the angle of the points in the curve
#                             : 'linear'/default -- w0->w1 varies with the length of the curve linearly
# @ Placement : [0,0] at the center of the racetrack
# =================================================================

class my_racetrack_euler_bend :
    def __init__(self,layer_wg=1,w1=0.45,w0=0.45,R1=5,R0=5,R2=10,dLx=0,dLy=0):
        with nd.Cell(instantiate=False) as C:

            euler_bend = my_euler_wg2wg(layer_wg=layer_wg,R0=R0,R1=R1,R2=R2,Win=w0,dW=(w1-w0),width_type='linear')
            euler_bend.cell.put(dLx/2,-dLy/2-euler_bend.sz[1],0)
            euler_bend.cell.put(dLx/2, dLy/2+euler_bend.sz[1],0,flip=1)
            euler_bend.cell.put(-dLx/2,dLy/2+euler_bend.sz[1],180)
            euler_bend.cell.put(-dLx/2,-(dLy/2+euler_bend.sz[1]),180,flip=1)

            ## placing the attching waveguide ##

            nd.strt(length=dLx,width=w0,layer=layer_wg).put(-dLx/2,dLy/2+euler_bend.sz[1],0)
            nd.strt(length=dLx,width=w0,layer=layer_wg).put(-dLx/2,-dLy/2-euler_bend.sz[1],0)
            nd.strt(length=dLy,width=w1,layer=layer_wg).put(-dLx/2-euler_bend.sz[0],-dLy/2,90)
            nd.strt(length=dLy,width=w1,layer=layer_wg).put( dLx/2+euler_bend.sz[0],-dLy/2,90)

        self.sz = [dLx+2*euler_bend.sz[0],dLy+2*euler_bend.sz[1]]
        self.cell = C

# =================================================================
# @ File : <mx_structure_lib.py>
# @ Device: coupler connected with Euler bends
# @ Parameters : * layer    : layer of the coupler
#              : * w_wg     : the width of the waveguide connected to the outside
#              : * w_cp     : the width of the coupler
#              : * dLc      : for straight coupler, the coupling length
#              : * dAc      : for bend coupler, the coupling angle
# =================================================================

class my_euler_coupler : ## 90
    def __init__(self,layer_wg=1,w_wg=0.45,w_cp=0.45,Rmax=10,R_cp=5,dLc=0,dAc=np.pi/5,theta_attach=np.pi/4,coupler_type = 'DC') :
        with nd.Cell(instantiate=False) as C:
            if (coupler_type=='straight' or coupler_type=='s' or coupler_type=='DC'):
                nd.strt(length=dLc,width=w_cp,layer=layer_wg).put(-dLc/2,0,0)
                dx_attatch = dLc/2
                dy_attach = 0
                theta_couple = 0

            elif (coupler_type=='bend' or coupler_type=='b' or coupler_type=='BDC'):
                mfl.my_std_ring(layer=layer_wg,radius=R_cp, width = w_cp, theta_start = 270-dAc/2/np.pi*180, theta_stop=270+dAc/2/np.pi*180, n_points = 256).frame.put(0,R_cp,0)
                theta_couple = dAc/2
                dx_attatch = R_cp*np.sin(theta_couple)
                dy_attach = R_cp-R_cp*np.cos(theta_couple)
            else :
                theta_couple = 0
                dx_attatch = 0
                dy_attach = 0

            euler_coupler = my_euler_wg2wg(layer_wg=layer_wg,bend_angle=theta_attach-theta_couple,R0=R_cp,R1=Rmax,Win=w_cp,dW=(w_wg-w_cp),bend_type='single',width_type='linear')
            el = euler_coupler.cell.put(dx_attatch,dy_attach,theta_couple/np.pi*180)
            er = euler_coupler.cell.put(-dx_attatch,dy_attach,180-theta_couple/np.pi*180,flip=1)

            euler_bend = my_euler_wg2wg(layer_wg=layer_wg,bend_angle=-theta_attach,R0=Rmax,R1=Rmax/2,Win=w_wg,dW=0,width_type='linear')
            br = euler_bend.cell.put('a0',el.pin['b0'].xya())
            bl = euler_bend.cell.put('a0',er.pin['b0'].xya(),flip=1)

            nd.Pin(name='a1',pin=bl.pin['b0']).put()
            nd.Pin(name='b1',pin=br.pin['b0']).put()

            ## placing the attching waveguide ##



        #self.sz = [dLx+2*euler_bend.sz[0],dLy+2*euler_bend.sz[1]]
        self.cell = C