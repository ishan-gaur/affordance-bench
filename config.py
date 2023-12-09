from pathlib import Path

EXP_DIR = Path.cwd() / "top_exp"
SCENE_IMAGES_FOLDER = 'rgb_images'
GIGA_AFF_MESH_FOLDER = 'grasps'
GIGA_IMAGES_FOLDER = 'grasp_images'
VRB_IMAGES_FOLDER = 'vrb'

EVAL_FILE = EXP_DIR.name + 'evals.tsv'
TRIAL_ID, RUN_PATH, GIGA_PATH, VRB_PATH = 'trial_id', 'run_path', 'giga_image', 'vrb_image'
NUM_SAME, ANNOTATED, CORRUPTED = 'num_same', 'is_annotated', 'corrupted'
ID_COLS = [TRIAL_ID, RUN_PATH, GIGA_PATH, VRB_PATH, ANNOTATED, CORRUPTED]
POS_MODES, DIR_MODES, NUM_FP = 'pos_modes', 'dir_modes', 'num_false_positives'
_common_cols = [POS_MODES, DIR_MODES, NUM_FP] # need to be annotated for each
GIGA_PREFIX, VRB_PREFIX = 'giga_', 'vrb_'
GIGA_COLS, VRB_COLS = [GIGA_PREFIX + c for c in _common_cols], [VRB_PREFIX + c for c in _common_cols]
ANNOTATION_COLS = [NUM_SAME] + GIGA_COLS + VRB_COLS
EVAL_COLS = ID_COLS + ANNOTATION_COLS

SIM_OBJECTS = 5