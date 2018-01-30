from collections import defaultdict
from enum import Enum

import solid

class Box:
    def __init__(self, width, length, height, wall_thickness):
        self.width = width
        self.length = length
        self.height = height
        self.wall_thickness = wall_thickness
        self.ornaments = defaultdict(list)

    def add_ornament(self, face, ornament):
        self.ornaments[face].append(ornament)

    def render_wall(self, face):
        x, y = face.get_width_length_on_plane(self.width, self.length, self.height)
        return solid.cube([x, y, self.wall_thickness])

    def render(self):
        walls = []
        for face in Face:
            wall = self.render_wall(face)
            wall_holes = []
            wall_adds = []
            x, y = face.get_width_length_on_plane(self.width, self.length, self.height)
            for ornament in self.ornaments[face]:
                hole, add = ornament.render(x, y, self.wall_thickness)
                if ornament.SIDE == Side.INTERNAL:
                    hole = solid.translate([0, 0, self.wall_thickness])(solid.scale([1, 1, -1])(hole))
                    add = solid.translate([0, 0, self.wall_thickness])(solid.scale([1, 1, -1])(add))
                wall_holes += [hole]
                wall_adds += [add]
            wall = wall - solid.union()(wall_holes) + solid.union()(wall_adds)
            walls += [self.rotate_wall_to_face(wall, face)]

        return solid.union()(walls)

    def rotate_wall_to_face(self, wall, face):
        """Given a wall, assumed to be laying on the xy plane, rotate it to the correct face"""
        if face == Face.BOTTOM:
            return solid.translate([self.width, 0,self.wall_thickness])(
                solid.rotate(a=180, v=[0, 1, 0])(wall)
            )
        elif face == Face.TOP:
            return solid.translate([0, 0, self.height-self.wall_thickness])(wall)
        elif face == Face.FRONT:
            return solid.translate([0, self.wall_thickness, 0])(
                solid.rotate(a=90, v=[1, 0, 0])(wall)
            )
        elif face == Face.BACK:
            return solid.translate([0, self.length-self.wall_thickness, self.height])(
                solid.rotate(a=-90, v=[1, 0, 0])(wall)
            )
        elif face == Face.LEFT:
            return solid.translate([self.wall_thickness, 0, 0])(
                solid.rotate(a=-90, v=[0, 1, 0])(wall)
            )
        elif face == Face.RIGHT:
            return solid.translate([self.width-self.wall_thickness, 0, self.height])(
                solid.rotate(a=90, v=[0, 1, 0])(wall)
            )


class RoundedBox(Box):
    def __init__(self, width, length, height, wall_thickness, corner_radius=None, corner_segments=24):
        super().__init__(width, length, height, wall_thickness)

        if not corner_radius or corner_radius >= self.wall_thickness * .5:
            corner_radius = self.wall_thickness * .5 - .01

        self.corner_radius = corner_radius
        self.corner_segments = corner_segments

    def render_wall(self, face):
        x, y = face.get_width_length_on_plane(self.width, self.length, self.height)
        # To get rid of some openscad sphere artifacts, we need to make sure all spheres are oriented the same way
        sphere_rot = 0 if face in (Face.BOTTOM, Face.TOP) else 90
        sphere_v = (0, 1, 0) if face in (Face.LEFT, Face.RIGHT) else (1, 0, 0)
        return solid.translate([self.corner_radius, self.corner_radius, self.corner_radius])(
            solid.minkowski()(
                solid.cube([
                    x-(self.corner_radius*2),
                    y-(self.corner_radius*2),
                    self.wall_thickness-(self.corner_radius*2)
                ]),
                solid.rotate(a=sphere_rot, v=sphere_v)(
                    solid.sphere(r=self.corner_radius, segments=self.corner_segments)
                )
            )
        )


class Face(Enum):
    BOTTOM = (0, 0, 0, 1, 1, 0)
    TOP = (0, 0, 1, 1, 1, 0)
    FRONT = (0, 0, 0, 1, 0, 1)
    BACK = (0, 1, 0, 1, 0, 1)
    LEFT = (0, 0, 0, 0, 1, 1)
    RIGHT = (1, 0, 0, 0, 1, 1)

    def get_width_length_on_plane(self, width, length, height):
        """Returns am x,y tuple corresponding to the size of the face if it was laying flat on the x,y plane"""
        if self in (Face.BOTTOM, Face.TOP):
            return width, length
        elif self in (Face.LEFT, Face.RIGHT):
            return height, length
        elif self in (Face.FRONT, Face.BACK):
            return width, height


class Side(Enum):
    EXTERNAL = 1
    INTERNAL = 2


class Ornament:
    def render(self, width, length, thickness):
        pass
