import pandas as pd
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

# Need to add directional and positional modes
# Need to run experiments with more grasps for 

import utils
from config import ANNOTATED, GIGA_PREFIX, VRB_PREFIX, NUM_SAME, POS_MODES, CORRUPTED
import components

eval_df = utils.setup()

total_samples = len(eval_df)
annotated_samples = eval_df[ANNOTATED].sum()
corrupted_samples = eval_df[CORRUPTED].sum()
total_samples = len(eval_df) - corrupted_samples
remaining_samples = total_samples - annotated_samples

st.header("Annotation Samples")
st.subheader(f"Remaining: {remaining_samples}; Annotated: {annotated_samples}; Total: {total_samples}")

if remaining_samples == 0:
    st.success("All Done!")
else:
    eval_sample = eval_df[~eval_df[ANNOTATED] & ~eval_df[CORRUPTED]].iloc[0]

    col1, col2 = st.columns([1, 1])
    submit = st.button('Submit')
    with col1:
        st.image(str(eval_sample['giga_image']), caption='Giga Image')
        eval_sample = components.common_cols(eval_sample, submit, prefix=GIGA_PREFIX)
    with col2:
        st.image(str(eval_sample['vrb_image']), caption='VRB Image')
        eval_sample = components.common_cols(eval_sample, submit, prefix=VRB_PREFIX)

    if submit:
        try:
            giga_grasp = [int(s) for s in eval_sample[GIGA_PREFIX + POS_MODES].split(',')]
            vrb_grasp = [int(s) for s in eval_sample[VRB_PREFIX + POS_MODES].split(',')]
            if len(giga_grasp) != len(vrb_grasp):
                raise ValueError("Lengths of giga and vrb grasps are not the same")
            eval_sample[NUM_SAME] = sum([g > 0 and v > 0 for g, v in zip(giga_grasp, vrb_grasp)])
            eval_df = utils.update_eval_entry(eval_sample, overwrite=True)
            streamlit_js_eval(js_expressions="parent.window.location.reload()")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            def mark_as_corrupted():
                eval_sample[CORRUPTED] = True
                eval_df = utils.update_eval_entry(eval_sample, overwrite=True)
            st.button("Mark as Corrupted", on_click=mark_as_corrupted)

st.header("Final Dataframe")
st.write(eval_df)
if st.button("Save Checkpoint"):
    timestamp = pd.Timestamp.now().strftime("%Y%m%d%H%M%S")
    eval_df.to_csv(f"evals_checkpoint_{timestamp}.tsv", sep='\t', index=False)
    st.success("Checkpoint saved!")
