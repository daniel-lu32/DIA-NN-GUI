import streamlit as st
import pandas as pd
import numpy as np
from hpc_manager import RemoteProjectFileSystem

from utils import get_fs

st.title("DIA-NN GUI")

fs = get_fs()

selected_project = st.selectbox("Select Project:", options=fs.list_projects())

t1, t2, t3 = st.tabs(["Upload Data Files", "Upload Spectral Libraries", "Configure Search Parameters and Run Search"])

with t1:
    st.subheader("Data Files")
    df = pd.DataFrame(fs.list_data_files(selected_project), columns=['Data Files'])
    st.dataframe(df, use_container_width=True, hide_index=True)

    @st.experimental_dialog("Upload Data Files")
    def add_dialogue():
        data_files = st.file_uploader(label="Upload Data Files", accept_multiple_files=True)
        column1, column2 = st.columns(2)
        with column1:
            if st.button("Upload", use_container_width=True, type='primary', key="data_add_dialogue_upload"):
                for file in data_files:
                    fs.add_data_file(selected_project, file.name, file.getvalue().decode("utf-8"))
                st.rerun()
        with column2:
            if st.button("Cancel", use_container_width=True, type='secondary', key="data_add_dialogue_cancel"):
                st.rerun()
    if st.button("Add", use_container_width=True, type='primary', key="data_add"):
        add_dialogue()

with t2:
    st.subheader("Spectral Libraries")
    @st.experimental_dialog("Upload Spectral Libraries")
    def add_dialogue():
        spec_lib_files = st.file_uploader(label="Upload Spectral Libraries", type=[".txt", ".csv", ".tsv", ".xls", ".speclib", ".sptxt", ".msp"], accept_multiple_files=True)
        column1, column2 = st.columns(2)
        with column1:
            if st.button("Upload", use_container_width=True, type='primary', key="spec_lib_add_dialogue_upload"):
                for file in spec_lib_files:
                    fs.add_spec_lib(selected_project, file.name, file.getvalue().decode("utf-8"))
                st.rerun()
        with column2:
            if st.button("Cancel", use_container_width=True, type='secondary', key="spec_lib_add_dialogue_cancel"):
                st.rerun()
    if st.button("Add", use_container_width=True, type='primary', key="spec_lib_add"):
        add_dialogue()
with t3:
    st.subheader("Search Parameters")
# @st.experimental_dialog("Upload Search")
# def upload_prompt():
#     column1, column2 = st.columns(2)
#     with column1:
#         if st.button("Confirm Search", use_container_width=True, type='secondary'):
#             fs.add_search(selected_project, search_name, search_parameters)
#             st.rerun()
#     with column2:
#         if st.button("Cancel", use_container_width=True, type='primary'):
#             st.rerun()
#
# if st.button("Configure Search Parameters", use_container_width=True, type='primary'):
#     upload_prompt()