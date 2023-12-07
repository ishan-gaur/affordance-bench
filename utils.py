from datetime import datetime
from pathlib import Path
from warnings import warn

import numpy as np
import pandas as pd

from config import EXP_DIR, GIGA_IMAGES_FOLDER, VRB_IMAGES_FOLDER
from config import EVAL_FILE, EVAL_COLS, TRIAL_ID, RUN_PATH, GIGA_PATH, VRB_PATH, ANNOTATED

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
            TRIAL_ID: trials,
            RUN_PATH: [run_path] * len(trials),
            GIGA_PATH: giga_paths,
            VRB_PATH: vrb_images
        })

        update_eval_df(update_df, overwrite=False)

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
    eval_df = pd.read_csv(eval_path, sep='\t') if eval_path.exists() else pd.DataFrame(columns=EVAL_COLS)

    missing_cols = set(EVAL_COLS) - set(eval_df.columns)
    for col in missing_cols:
        eval_df[col] = False if col == ANNOTATED else np.nan

    extra_cols = set(eval_df.columns) - set(EVAL_COLS)
    if extra_cols:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_path = eval_path.with_suffix(f".{timestamp}.tsv")
        eval_df.to_csv(backup_path, sep='\t', index=False)
        print(f"Warning: Extra columns {extra_cols} found in eval_df. A backup has been saved as '{backup_path}'.")
        eval_df = eval_df[EVAL_COLS]

    eval_df[ANNOTATED] = ~eval_df.isnull().any(axis=1)
    save_eval_df(eval_df)
    return eval_df

def update_eval_df(update_df, overwrite):
    eval_df = load_eval_df()
    if overwrite:
        new_trials = set(update_df[TRIAL_ID])
        eval_df = eval_df[~eval_df[TRIAL_ID].isin(new_trials)]
    else:
        existing_trials = set(eval_df[TRIAL_ID])
        update_df = update_df[~update_df[TRIAL_ID].isin(existing_trials)]
    eval_df = pd.concat([eval_df, update_df], ignore_index=True)
    save_eval_df(eval_df)
    return eval_df

def update_eval_entry(entry, overwrite):
    trial_id = entry[TRIAL_ID]
    eval_df = load_eval_df()
    if trial_id in eval_df[TRIAL_ID].values:
        if overwrite:
            eval_df[eval_df[TRIAL_ID] == trial_id] = entry
        else:
            warn(f"Overwrite set to true and trial id {trial_id} exists.")
    else:
        eval_df = pd.concat([eval_df, pd.DataFrame([entry])], ignore_index=True)
    save_eval_df(eval_df)
    return eval_df
