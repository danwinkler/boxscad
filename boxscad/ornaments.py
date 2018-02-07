from boxscad import Ornament, Side

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


class StandOffs(Ornament):
    SIDE = Side.INTERNAL

    def __init__(self, width, length, height, hole_radius, attached_to_wall=False, standoff_wall_percentage=1.5, wall_hole_depth=0):
        self.width = width
        self.length = length
        self.height = height
        self.hole_radius = hole_radius
        self.attached_to_wall = attached_to_wall
        self.standoff_wall_percentage = standoff_wall_percentage
        self.wall_hole_depth = wall_hole_depth

    def render(self, width, length, thickness):
        if self.attached_to_wall:
            raise NotImplementedError('attached_to_wall is not yet implemented')

        standoff = solid.cylinder(r=self.hole_radius*(self.standoff_wall_percentage+1), h=self.height, segments=24)
        hole = solid.translate([0, 0, -self.wall_hole_depth])(
            solid.cylinder(r=self.hole_radius, h=self.height+self.wall_hole_depth+1, segments=24)
        )
        standoff -= hole

        x_offset = (width - self.width) * .5
        y_offset = (length - self.length) * .5

        return solid.union()(
            solid.translate([x_offset, y_offset, thickness])(hole),
            solid.translate([x_offset + self.width, y_offset, thickness])(hole),
            solid.translate([x_offset + self.width, y_offset + self.length, thickness])(hole),
            solid.translate([x_offset, y_offset + self.length, thickness])(hole)
        ), solid.union()(
            solid.translate([x_offset, y_offset, thickness])(standoff),
            solid.translate([x_offset+self.width, y_offset, thickness])(standoff),
            solid.translate([x_offset+self.width, y_offset+self.length, thickness])(standoff),
            solid.translate([x_offset, y_offset+self.length, thickness])(standoff)
        )


class SquareHole(Ornament):
    #SIDE = Side.INTERNAL

    def __init__(self, x, y, width, length):
        self.x = x
        self.y = y
        self.width = width
        self.length = length

    def render(self, width, length, thickness):
        return solid.translate([self.x, self.y, -1])(
            solid.cube([self.width, self.length, thickness+2])
        ), []
