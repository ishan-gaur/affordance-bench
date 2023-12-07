from pathlib import Path
from warnings import warn

import pandas as pd

from config import EXP_DIR, GIGA_IMAGES_FOLDER, VRB_IMAGES_FOLDER
from config import EVAL_FILE

def setup():
    runs = get_all_runs(EXP_DIR)
    for run_path in runs:
        giga_path = run_path / GIGA_IMAGES_FOLDER
        vrb_path = run_path / VRB_IMAGES_FOLDER
        if not giga_path.exists() or not vrb_path.exists():
            if not giga_path.exists():
                warn(f"Missing GIGA grasp images: {giga_path} does not exist.")
            if not vrb_path.exists():
                warn(f"Missing VRB grasp images: {vrb_path} does not exist.")
            continue

        trials, giga_paths, vrb_images, corrupted = get_run_trials(run_path)
        if corrupted:
            continue

        update_df = pd.DataFrame({
            'trial_id': trials,
            'run_path': [run_path] * len(trials),
            'giga_image': giga_paths,
            'vrb_image': vrb_images
        })

        update_eval_df(update_df)

    return load_eval_df()

def get_all_runs(dir):
    return list(filter(lambda f: f.is_dir(), dir.iterdir()))

def get_run_trials(run_folder):
    giga_images = list((run_folder / GIGA_IMAGES_FOLDER).glob('*.png'))
    vrb_images = list((run_folder / VRB_IMAGES_FOLDER).glob('*.png'))
    giga_images.sort(key=lambda x: x.stem)
    vrb_images.sort(key=lambda x: x.stem)

    giga_stems = {g.stem for g in giga_images}
    vrb_stems = {v.stem for v in vrb_images}
    matching_stems = giga_stems.intersection(vrb_stems)

    corrupted = len(matching_stems) != len(giga_images) or len(matching_stems) != len(vrb_images)
    if corrupted:
        warn(f"Image pairs in {run_folder} have mismatched stems.")

    trial_names = [f"{run_folder.name}_{stem}" for stem in matching_stems]
    giga_paths = list(filter(lambda x: x.stem in matching_stems, giga_images))
    vrb_paths = list(filter(lambda x: x.stem in matching_stems, vrb_images))

    return trial_names, giga_paths, vrb_paths, corrupted

def get_eval_file_path():
    return EXP_DIR / EVAL_FILE

def save_eval_df(eval_df):
    eval_path = get_eval_file_path()
    if not eval_path.exists():
        eval_path.touch()
    eval_df.to_csv(get_eval_file_path(), sep='\t', index=False)

def load_eval_df():
    eval_path = get_eval_file_path()
    if not eval_path.exists():
        eval_df = pd.DataFrame(columns=['trial_id', 'run_path', 'giga_image', 'vrb_image'])
        save_eval_df(eval_df)
    return pd.read_csv(eval_path, sep='\t')

def update_eval_df(update_df, overwrite=False):
    eval_df = load_eval_df()
    if overwrite:
        new_trials = set(update_df['trial_id'])
        eval_df = eval_df[~eval_df['trial_id'].isin(new_trials)]
    else:
        existing_trials = set(eval_df['trial_id'])
        update_df = update_df[~update_df['trial_id'].isin(existing_trials)]
    eval_df = pd.concat([eval_df, update_df], ignore_index=True)
    save_eval_df(eval_df)
    return eval_df