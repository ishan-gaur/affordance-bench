import streamlit as st
from pathlib import Path
import pickle as pkl
import random
from PIL import Image
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Setup Dataset
experiment_folder = [
    "./horizontal_exp",
    "./single_exp",
    "./top_exp",
    "./pile_exp"
]
experiment_folder = [Path(f).resolve() for f in experiment_folder]

preferences_path = Path.cwd() / "preferences.pkl"
if not preferences_path.exists():
    all_trials = {}
else:
    all_trials = pkl.load(preferences_path.open("rb"))

for folder_path in experiment_folder:
    experiment_directories = [d for d in folder_path.iterdir() if d.is_dir()]
    for experiment_directory in experiment_directories:
        grasp_images_dir = experiment_directory / "grasp_images"
        vrb_dir = experiment_directory / "vrb"
        grasp_images_files = [f.name for f in grasp_images_dir.iterdir() if f.is_file()]
        vrb_files = [f.name for f in vrb_dir.iterdir() if f.is_file()]
        for grasp_images_file in grasp_images_files:
            if grasp_images_file in vrb_files:
                trial_id = f"{folder_path.name}_{experiment_directory.name}_{grasp_images_file}"
                if trial_id not in all_trials:
                    all_trials[trial_id] = {
                        "grasp_images": str(grasp_images_dir / grasp_images_file),
                        "vrb": str(vrb_dir / grasp_images_file),
                        "preference": [0, 0]
                    }
pkl.dump(all_trials, preferences_path.open("wb"))

# Show GIGA and VRB images side by side and record the user preference
# Find the minimum preference count
min_preference_count = min([trial_info["preference"][0] + trial_info["preference"][1] for trial_info in all_trials.values()])

# Get the trial IDs with the minimum preference count
min_preference_trials = [trial_id for trial_id, trial_info in all_trials.items() if trial_info["preference"][0] + trial_info["preference"][1] == min_preference_count]

# Pick a random trial ID from the ones with the minimum preference count
random_trial_id = random.choice(min_preference_trials)
giga_image_path = all_trials[random_trial_id]["grasp_images"]
vrb_image_path = all_trials[random_trial_id]["vrb"]

# Load the images
giga_image = Image.open(giga_image_path)
vrb_image = Image.open(vrb_image_path)

# Resize the images
resized_giga_image = giga_image.resize((400, 400))
resized_vrb_image = vrb_image.resize((400, 400))

# Display the images side by side in two columns
col1, col2 = st.columns(2)
with col1:
    st.image(resized_giga_image, caption="GIGA Image", width=400)
    if st.button("GIGA Preference"):
        all_trials[random_trial_id]["preference"][0] += 1
        pkl.dump(all_trials, preferences_path.open("wb"))

with col2:
    st.image(resized_vrb_image, caption="VRB Image", width=400)
    if st.button("VRB Preference"):
        all_trials[random_trial_id]["preference"][1] += 1
        pkl.dump(all_trials, preferences_path.open("wb"))

# Show the preference results
st.write("Preference Results")

# Create a bar chart of the preferences
preference_data = []
for trial_id, trial_info in all_trials.items():
    folder_name = trial_id.split("_")[0]
    preference_count = trial_info["preference"]
    preference_data.append((folder_name, preference_count[0], preference_count[1]))

df = pd.DataFrame(preference_data, columns=["Experiment Directory", "GIGA Preference", "VRB Preference"])
df = df.melt("Experiment Directory", var_name="Preference", value_name="Count")
plot = sns.barplot(x="Experiment Directory", y="Count", hue="Preference", data=df)
plt.xlabel("Experiment Directory")
plt.ylabel("Preference Count")
plt.title("Preference Results")
plt.legend(["GIGA Preference", "VRB Preference"])
st.pyplot(plot.get_figure())