from pathlib import Path

EXP_DIR = Path.cwd() / "experiments"
SCENE_IMAGES_FOLDER = 'rgb_images'
GIGA_AFF_MESH_FOLDER = 'grasps'
GIGA_IMAGES_FOLDER = 'grasp_images'
VRB_IMAGES_FOLDER = 'vrb'

EVAL_FILE = 'evals.tsv'
TRIAL_ID, RUN_PATH, GIGA_PATH, VRB_PATH = 'trial_id', 'run_path', 'giga_image', 'vrb_image'
NUM_SAME, ANNOTATED = 'num_same', 'is_annotated'
SAMPLE_COLS = [TRIAL_ID, RUN_PATH, GIGA_PATH, VRB_PATH, NUM_SAME, ANNOTATED]
OBJ_MODES, NUM_FP = 'modes_per_object', 'num_false_positives'
_common_cols = [OBJ_MODES, NUM_FP] # need to be annotated for each
GIGA_PREFIX, VRB_PREFIX = 'giga_', 'vrb_'
GIGA_COLS, VRB_COLS = [GIGA_PREFIX + c for c in _common_cols], [VRB_PREFIX + c for c in _common_cols]

EVAL_COLS = SAMPLE_COLS + GIGA_COLS + VRB_COLS

SIM_OBJECTS = 5