import numpy as np
import trimesh
from pathlib import Path

exp_folder = Path('/Users/ishangaur/23-12-06-04-38-25')
grasps_folder = exp_folder / 'grasps'
for grasp_path in grasps_folder.iterdir():
    if grasp_path.suffix != '.obj':
        continue
    grasp_mesh = trimesh.load_mesh(grasp_path)
    scene = trimesh.Scene()
    scene.add_geometry(grasp_mesh)
    size = grasp_mesh.bounding_box.extents[0]
    scene.set_camera(distance=2.0 * size, angles=[np.pi / 3, 0, 0])
    png = scene.save_image()
    with open(grasp_path.with_suffix('.png'), 'wb') as f:
        f.write(png)
