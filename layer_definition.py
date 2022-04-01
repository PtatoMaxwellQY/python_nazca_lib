import nazca as nd
import numpy as np

class AMF_tapout :
    LAYER_WG_RIB = 10
    LAYER_WG_GRATING_COUPLER = 11
    LAYER_WG_SLAB = 12
    LAYER_METAL = 105
    LAYER_HEATER = 115
    LAYER_VIA2META1 = 120
    LAYER_METAL_2 = 125
    LAYER_METAL_PAD = 13
    LAYER_WG_SI3N4 = 54
    STD_SMWG_WIDTH = 0.45

    lib_path = 'mx_lib\\GDS\\'

    def __init__ (self):
        nd.add_layer(name='Rib', layer=self.LAYER_WG_RIB)
        nd.add_layer2xsection(xsection='Rib', layer='Rib')
        self.XS_WG_RIB = 'Rib'
        nd.add_layer(name='Slab', layer=self.LAYER_WG_SLAB)
        nd.add_layer2xsection(xsection='Slab', layer='Rib')
        nd.add_layer2xsection(xsection='Slab', layer='Slab',leftedge=(0.5, 2), rightedge=(-0.5, -2))
        self.XS_WG_SLAB = 'Slab'
        nd.add_layer(name='Heater', layer=self.LAYER_HEATER)
        nd.add_layer2xsection(xsection='Heater', layer='Heater')
        self.XS_HEATER = 'Heater'

        nd.add_layer(name='METAL', layer=self.LAYER_METAL)
        nd.add_layer2xsection(xsection='METAL', layer='METAL')
        self.XS_METAL = 'METAL'

    W_METAL_MIN = 5
    SPACING_METAL_MIN = 8
    W_HEATER_MIN = 3

class ANT_Tapout :
    LAYER_WG_RIB = 1
    LAYER_METAL = 12
    LAYER_HEATER = 11
    LAYER_METAL_PAD = 13

    lib_path = 'mx_lib\\GDS\\'

    def __init__ (self):
        nd.add_layer(name='Strip', layer=1)
        nd.add_layer2xsection(xsection='Strip', layer='Strip')
        self.XS_WG_RIB = 'Strip'
        self.XS_WG_STRIP = 'Strip'
        self.LAYER_WG_STRIP = 'Strip'
        self.LAYER_WG_RIB = 'Strip'
        
        nd.add_layer(name='Heater', layer=11)
        nd.add_layer2xsection(xsection='Heater', layer='Heater')
        self.XS_HEATER = 'Heater'
        self.LAYER_HEATER = 'Rib'

        nd.add_layer(name='METAL', layer=12)
        nd.add_layer2xsection(xsection='METAL', layer='METAL')
        self.XS_METAL = 'METAL'
        self.LAYER_METAL = 'METAL'

    STD_SMWG_WIDTH = 0.45
    W_METAL_MIN = 5
    SPACING_METAL_MIN = 8
    W_HEATER_MIN = 3

    class CUMEC_ACTIVE :
        LAYER_METAL = 12
        LAYER_HEATER = 11
        LAYER_METAL_PAD = 13
        STD_SMWG_WIDTH = 0.45

        lib_path = 'mx_lib\\GDS\\'

        def __init__ (self):
            nd.add_layer(name='Strip', layer=(31,1)) ## defining the strip waveguide core area
            nd.add_layer(name='FETCH_CLD', layer=(31,2)) ## defining the etched side for strip waveguide core area
            nd.add_layer2xsection(xsection='Strip', layer='Strip')
            nd.add_layer2xsection(xsection='Strip', layer='FETCH_CLD',leftedge=(0.5, 3), rightedge=(-0.5, -3))
            self.XS_WG_STRIP = 'Strip'
            self.LAYER_WG_STRIP = 'Strip' # 31,1

            nd.add_layer(name='Rib', layer=(32,1)) ## defining the Rib area with 70nm etched waveguide core area
            nd.add_layer(name='SETCH_CLD', layer=(32,2)) ## defining the etched side for strip waveguide core area
            nd.add_layer2xsection(xsection='Rib', layer='Rib')
            nd.add_layer2xsection(xsection='Rib', layer='SETCH_CLD',leftedge=(0.5, 3), rightedge=(-0.5, -3))
            nd.add_layer2xsection(xsection='Rib', layer='FETCH_CLD',leftedge=(0.5, 6), rightedge=(-0.5, -6))
            self.XS_WG_RIB = 'Rib'
            self.LAYER_WG_RIB = 'Rib' # 31,1
            
            nd.add_layer(name='Rib_2', layer=(33,1)) ## defining the Rib area with 150nm etched waveguide core area
            nd.add_layer2xsection(xsection='Rib_2', layer='Rib2')
            self.XS_WG_RIB_2 = 'Rib_2'
            self.LAYER_WG_RIB_2 = 'Rib2' # 31,1

            nd.add_layer(name='Heater', layer=(19,0))
            nd.add_layer2xsection(xsection='Heater', layer='Heater')
            self.XS_HEATER = 'Heater'
            self.LAYER_HEATER = 'Heater' # 31,1

            nd.add_layer(name='METAL', layer=(11,1))
            nd.add_layer2xsection(xsection='METAL', layer='METAL')
            self.XS_METAL = 'METAL'

            nd.add_layer(name='METAL_2', layer=(12,1))
            nd.add_layer2xsection(xsection='METAL', layer='METAL')
            self.XS_METAL_2 = 'METAL_2'

            nd.add_layer(name='Via', layer=(51,0))
            nd.add_layer2xsection(xsection='Via', layer='Via')
            self.XS_METAL_2 = 'Via'

        W_METAL_MIN = 5
        SPACING_METAL_MIN = 8
        W_HEATER_MIN = 3