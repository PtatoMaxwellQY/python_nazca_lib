####

import nazca as nd
import numpy as np

## Polygon Function ##
def _my_polygon (layer_wg,vtx) : 
    sz_l = vtx.shape
    sz_l = sz_l[0]

    idx_seq = np.linspace(1,sz_l-1,sz_l-1)

    _points_ = [(vtx[0,0],vtx[0,1])]
    for idx in idx_seq:
        _point_cur_ = [(vtx[int(idx),0],vtx[int(idx),1])]
        _points_.extend(_point_cur_)
        
    frame = nd.Polygon(layer=layer_wg, points = _points_)
    
    return frame      

## generates a ring with center to ring's center ##
class my_std_ring :

    def __init__(self, layer = 1,radius = 10, width = 0.45, theta_start = 0, theta_stop=360, n_points = 1024):
        theta = np.linspace(theta_start,theta_stop,n_points)

        theta = theta/180*np.pi

        vtx_outer_x = np.cos(theta)*(radius+width/2)
        vtx_outer_y = np.sin(theta)*(radius+width/2)
        vtx_inner_x = np.cos(theta)*(radius-width/2)
        vtx_inner_y = np.sin(theta)*(radius-width/2)
        vtx_outer = np.c_[vtx_outer_x,vtx_outer_y]
        vtx_inner = np.c_[np.flip(vtx_inner_x),np.flip(vtx_inner_y)]
        vtx = np.r_[vtx_outer,vtx_inner]
        self.frame = _my_polygon(layer,vtx)


class my_std_racetrack :

    def __init__(self,layer=1,radius=10,L1=5,L2=5,width =0.45,n_points =256):
        with nd.Cell(instantiate=False) as C:
            arc = my_std_ring(layer=layer,radius=radius,width=width,theta_start=0,theta_stop=90,n_points=n_points)
            arc.frame.put( L1/2, L2/2,0)
            arc.frame.put(-L1/2, L2/2,90)
            arc.frame.put( L1/2,-L2/2,-90)
            arc.frame.put(-L1/2,-L2/2,180)
            nd.strt(length=L1,width=width,layer=layer).put(-L1/2,L2/2+radius,0)
            nd.strt(length=L1,width=width,layer=layer).put(-L1/2,-L2/2-radius,0)
            nd.strt(length=L2,width=width,layer=layer).put(-L1/2-radius,-L2/2,90)
            nd.strt(length=L2,width=width,layer=layer).put( L1/2+radius,-L2/2,90)
        self.cell = C


class poly_wg: 
        def __init__(self,vtx_line,width) :
            
            x = vtx_line[:,0]
            y = vtx_line[:,1]
            z = x + 1j*y

            dz = np.diff(z)
            dz = np.r_[dz,dz[-1]]

            dir_upper = -1j*np.real(dz) + np.imag(dz)
            dir_lower = -dir_upper

            p_upper = z + dir_upper*width/2/abs(dir_upper)
            p_lower = z + dir_lower*width/2/abs(dir_lower)

            vtx_upper = np.c_[np.real(p_upper),np.imag(p_upper)]
            vtx_lower = np.c_[np.real(p_lower),np.imag(p_lower)]

            self.vtx_upper = vtx_upper
            self.vtx_lower = vtx_lower
            self.vtx_middle = vtx_line
            self.width = width
            self.vtx = np.r_[vtx_upper,np.flip(vtx_lower,0)]
    

def my_poly_spiral(r,theta,coord,order,dL,R_max):
    K_ends = np.array([1/r[0],1/r[1]]) ## definition of the curvature, r[0] is the beginnin and r[1] is the ending
    L0 = np.abs(theta[0]-theta[1])/(K_ends[0] + (K_ends[1]-K_ends[0])*order/(order+1))
    L = np.linspace(0,L0,int(np.floor(L0/dL)+1)) ## L = [0:dL:L0];
    K = K_ends[0] + (K_ends[1] - K_ends[0])/np.power(L0,order)*(np.power(L0,order) - np.power(np.abs(L-L0),order))
    R = 1/K
     
    dir = np.sign(theta[1] - theta[0])
    dt = dir*dL/R

    theta_temp = np.cumsum(dt) + theta[0]

    x = np.zeros(len(L)) + coord[0]
    y = np.zeros(len(L)) + coord[1]
     
    idx = np.linspace(1,len(L)-1,len(L)-2+1)
    for _idx_ in idx :
        _idx_ = int(_idx_)
        x[_idx_] = x[_idx_-1] + dir*R[_idx_]*( np.sin(theta_temp[_idx_]) - np.sin(theta_temp[_idx_-1]))
        y[_idx_] = y[_idx_-1] - dir*R[_idx_]*( np.cos(theta_temp[_idx_]) - np.cos(theta_temp[_idx_-1]))

    x_end = x[len(x)-1]
    y_end = y[len(x)-1]
    x = np.r_[x[0],x[1:-2:10]]
    y = np.r_[y[0],y[1:-2:10]]

    x = np.r_[x,x_end]
    y = np.r_[y,y_end]


    vtx = np.c_[x,y]
    return vtx ## vtx = [vtx_x,vtx_y]
