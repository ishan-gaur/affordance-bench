import pandas as pd    
import streamlit as st
from config import *


def num_same(entry, submit):
    print(entry)
    num_same = st.number_input('Number Same', min_value=0, max_value=SIM_OBJECTS, 
                               value=entry[NUM_SAME], step=1)
    if submit:
        entry[NUM_SAME] = num_same
    return entry

def common_cols(entry, submit, prefix):
    def obj_modes(entry, submit):
        try:
            modes_list = entry[prefix + OBJ_MODES].split(",")
        except AttributeError:
            modes_list = [None] * SIM_OBJECTS
        if not all(isinstance(m, int) for m in modes_list) or len(modes_list) != SIM_OBJECTS:
            modes_list = [None] * SIM_OBJECTS

        st.subheader("Objects Left to Right")
        for i in range(SIM_OBJECTS):
            title = f'Modes for Object {i+1}'
            mode = st.number_input(title, min_value=0, step=1,
                                   value=modes_list[i], key=prefix+title)
            modes_list.append(mode)
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
