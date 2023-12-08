import pandas as pd    
import streamlit as st
from config import *


def num_same(entry, submit):
    num_same = st.number_input('Number Same', min_value=0, max_value=SIM_OBJECTS, 
                               value=entry[NUM_SAME], step=1)
    if submit:
        entry[NUM_SAME] = num_same
    return entry

def common_cols(entry, submit, prefix):
    def obj_modes(entry, submit):
        modes_str = entry.get(prefix + OBJ_MODES, "")

        st.subheader("Number of Modes per Object")
        modes_input = st.text_input("Enter comma-separated number of modes for each object, left to right, top to bottom",
                                     value=modes_str, key=prefix+"modes_input")
        modes_list = [int(m.strip()) if m.strip().isdigit() else None for m in modes_input.split(",")]

        if submit:
            entry[prefix + OBJ_MODES] = ",".join([str(m) if m is not None else "" for m in modes_list])
        return entry

    def num_false_positives(entry, submit):
        try:
            num_fp = int(entry[prefix + NUM_FP])
        except (ValueError, TypeError):
            num_fp = None

        title = f'Number of False Positives'
        num_fp = st.number_input(title, min_value=0, max_value=SIM_OBJECTS, step=1, value=num_fp,
                                 placeholder="Enter number of false positives", key=prefix+title)
        if submit:
            entry[prefix + NUM_FP] = num_fp
        return entry

    entry = obj_modes(entry, submit)
    entry = num_false_positives(entry, submit)
    return entry
