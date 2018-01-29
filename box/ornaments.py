from box import Ornament, Side

import solid


class InsetLid(Ornament):
    SIDE = Side.EXTERNAL

    def __init__(self, thickness, rim_thickness=None, margin=.1, depth_margin=.1):
        self.thickness = thickness
        self.rim_thickness = rim_thickness
        self.margin=margin
        self.depth_margin=depth_margin

    def render(self, width, length, thickness):
        rim_thickness = self.rim_thickness if self.rim_thickness else thickness * .5
        return [], solid.hole()(
            solid.translate([rim_thickness-self.margin, rim_thickness-self.margin, thickness-self.thickness-self.depth_margin])(
                solid.cube([
                    width - (rim_thickness*2) - (self.margin*2),
                    length - (rim_thickness*2) - (self.margin*2),
                    self.thickness + self.depth_margin + .1
                ])
            )
        )
