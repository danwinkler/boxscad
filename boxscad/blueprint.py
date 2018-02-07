import platform

import solid
from plumbum import local

from boxscad import Face





def get_openscad_windows():
    return local.get(
        local.path(local.env['ProgramFiles']) / 'OpenSCAD/openscad.exe',
        local.path(local.env['ProgramFiles(x86)']) / 'OpenSCAD/openscad.exe'
    )

def get_openscad():
    if platform.system() == 'Windows':
        return get_openscad_windows()
    else:
        # TODO
        pass

def render_openscad(
        output_filename,
        input_filename,
        width,
        height,
        center,
        face
    ):
    eye_locations = {
        Face.BOTTOM: (0, 0, -1),
        Face.TOP: (0, 0, 1),
        Face.LEFT: (-1, 0, 0),
        Face.RIGHT: (1, 0, 0),
        Face.FRONT: (0, -1, 0),
        Face.BACK: (0, 1, 0),
    }

    eye_distance = 252

    centerx, centery, centerz = center[0], center[1], center[2]
    eyex, eyey, eyez = eye_locations[face]

    eyex *= eye_distance
    eyey *= eye_distance
    eyez *= eye_distance

    eyex += centerx
    eyey += centery
    eyez += centerz

    openscad = get_openscad()
    openscad(
        '-o',
        output_filename,
        '--imgsize={},{}'.format(width, height),
        '--camera={},{},{},{},{},{}'.format(eyex, eyey, eyez, centerx, centery, centerz),
        '--preview=w',
        '--projection=o',
        input_filename
    )

def blueprint(folder_name, box):
    folder = local.path(folder_name)
    folder.mkdir()

    temp_scad = folder / 'temp.scad'
    solid.scad_render_to_file(box.render(), temp_scad)

    render_openscad(folder / 'front.png', temp_scad, 1000, 1000, box.center(), Face.FRONT)

    temp_scad.delete()
