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
    STD_SMWG_WIDTH = 0.5

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
        nd.add_layer(name='Rib', layer=self.LAYER_WG_RIB)
        nd.add_layer2xsection(xsection='Rib', layer='Rib')
        self.XS_WG_RIB = 'Rib'
        
        nd.add_layer(name='Heater', layer=self.LAYER_HEATER)
        nd.add_layer2xsection(xsection='Heater', layer='Heater')
        self.XS_HEATER = 'Heater'

        nd.add_layer(name='METAL', layer=self.LAYER_METAL)
        nd.add_layer2xsection(xsection='METAL', layer='METAL')
        self.XS_METAL = 'METAL'

    W_METAL_MIN = 5
    SPACING_METAL_MIN = 8
    W_HEATER_MIN = 3