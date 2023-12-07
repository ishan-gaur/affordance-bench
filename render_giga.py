import numpy as np
import trimesh
from pathlib import Path
import sys

if len(sys.argv) != 2:
    print("Usage: python render_giga.py <path/to/experiment/directory/>")
    sys.exit(1)

exp_folder = Path(sys.argv[1]).resolve()
for trial_folder in exp_folder.iterdir():
    if not trial_folder.is_dir():
        continue
    grasps_folder = trial_folder / 'grasps'
    image_folder = trial_folder / 'grasp_images'
    if not image_folder.exists():
        image_folder.mkdir()

    scene_size = None
    for grasp_path in grasps_folder.iterdir():
        if grasp_path.suffix != '.obj':
            continue
        grasp_mesh = trimesh.load_mesh(grasp_path)
        scene = trimesh.Scene()
        scene.add_geometry(grasp_mesh)

        if scene_size == None:
            scene_size = grasp_mesh.bounding_box.extents[0]
        scene.set_camera(distance=2.0 * scene_size, angles=[np.pi / 3, 0, 0])
        png = scene.save_image()

        image_path = image_folder / grasp_path.stem
        image_path = image_path.with_suffix('.png')
        with open(image_path, 'wb') as f:
            f.write(png)
